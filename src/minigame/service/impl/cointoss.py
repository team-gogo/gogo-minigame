import json
import random
import time

from fastapi import status, WebSocketException
from py_eureka_client.eureka_client import do_service_async
from sqlmodel.ext.asyncio.session import AsyncSession

from event.producer import EventProducer
from src.minigame.service.validation import BetValidationService
from src.minigame.presentation.schema.event import MinigameAdditionPoint
from src.cointoss.presentation.schema.cointoss import CoinTossBetReq
from src.minigame.service.bet import MinigameBetService
from src.cointoss.domain.model.coin_toss_result import CoinTossResult
from src.cointoss.domain.repository.coin_toss import CoinTossResultRepository
from src.minigame.domain.repository.minigame import MinigameRepository
from src.ticket.domain.repository.ticket import TicketRepository
from src.cointoss.presentation.schema.cointoss import CoinTossBetRes


class CoinTossMinigameBetServiceImpl(MinigameBetService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.minigame_repository = MinigameRepository(session)
        self.coin_toss_result_repository = CoinTossResultRepository(session)
        self.ticket_repository = TicketRepository(session)

    async def bet(self, stage_id, user_id, data: CoinTossBetReq):
        async with self.session.begin():
            bet_amount = data.amount

            # stage_id로 미니게임 조회
            minigame = await self.minigame_repository.find_by_stage_id(stage_id)
            if not minigame.is_active_yavarwee:
                raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason='Minigame not found')

            await BetValidationService.validate_minigame_status(minigame)

            # 유저 포인트 정보 가져오기
            response = await do_service_async('gogo-stage', f'/stage/api/point/{stage_id}?studentId={user_id}')
            if not response:
                raise WebSocketException(code=status.WS_1011_INTERNAL_ERROR, reason='gogo-stage no response')
            before_point = json.loads(response)['point']

            # 포인트 검사
            if bet_amount > before_point:
                raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason='bet amount too high')

            # 티켓 검사
            ticket = await self.ticket_repository.find_by_minigame_id_and_user_id_for_update(minigame.minigame_id, user_id)
            if ticket is None or ticket.coin_toss_ticket_amount <= 0:
                raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason='Not enough ticket')

            # 티켓 감소
            ticket.coin_toss_ticket_amount -= 1

            if result := random.choice([True, False]):
                await EventProducer.create_event(
                    'minigame_bet_addition_point',
                    MinigameAdditionPoint(
                        point=bet_amount,
                        user_id=user_id,
                    )
                )
                after_point = before_point + bet_amount
            else:
                await EventProducer.create_event(
                    'minigame_bet_minus_point',
                    MinigameAdditionPoint(
                        point=bet_amount,
                        user_id=user_id,
                    )
                )
                after_point = before_point - bet_amount

            await self.coin_toss_result_repository.save(
                CoinTossResult(
                    minigame_id=int(minigame.minigame_id),
                    student_id=int(user_id),
                    timestamp=int(time.time()),
                    bet_point=bet_amount,
                    result=result,
                    point=after_point
                )
            )

            return CoinTossBetRes(
                result=result,
                amount=after_point
            )