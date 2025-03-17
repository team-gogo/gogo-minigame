import json
import random
import time
import uuid

from fastapi import status, WebSocketException
from py_eureka_client.eureka_client import do_service_async
from sqlmodel.ext.asyncio.session import AsyncSession

from db import get_session
from event.producer import EventProducer
from src.minigame.domain.model.minigame import MinigameBetStatus
from src.minigame.service.validation import BetValidationService
from src.minigame.presentation.schema.event import MinigameAdditionPoint
from src.cointoss.presentation.schema.cointoss import CoinTossBetReq
from src.minigame.service.bet import MinigameBetService
from src.cointoss.domain.model.coin_toss_result import CoinTossResult
from src.cointoss.domain.repository.coin_toss import CoinTossResultRepository
from src.minigame.domain.repository.minigame import MinigameRepository
from src.ticket.domain.repository.ticket import TicketRepository
from src.cointoss.presentation.schema.cointoss import CoinTossBetRes
from src.ticket.service.ticket import TicketService


class CoinTossMinigameBetServiceImpl(MinigameBetService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.minigame_repository = MinigameRepository(session)
        self.coin_toss_result_repository = CoinTossResultRepository(session)
        self.ticket_repository = TicketRepository(session)
        self.ticket_service = TicketService

    async def bet(self, stage_id, user_id, data: CoinTossBetReq):
        async with self.session.begin():
            bet_amount = data.amount

            # stage_id로 미니게임 조회
            minigame = await self.minigame_repository.find_by_stage_id(stage_id)
            if not minigame.is_active_coin_toss:
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
            ticket_amount = await self.ticket_service(await get_session()).get_ticket_amount(user_id=user_id, stage_id=stage_id)
            if ticket_amount is None or ticket_amount.coinToss <= 0:
                raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason='Not enough ticket')
            ticket = await self.ticket_repository.find_ticket_amount_by_stage_id_and_user_id(stage_id=stage_id, user_id=user_id)

            # 티켓 감소
            ticket.coin_toss_ticket_amount -= 1

            uuid_ = str(uuid.uuid4())

            #     "error": "unsupported operand type(s) for &: 'str' and 'int'" 해결

            if result := random.choice([True, False]):
                await EventProducer.create_event(
                    topic='minigame_bet_addition_point',
                    key=uuid_,
                    value=MinigameAdditionPoint(
                        id=uuid_,
                        point=bet_amount,
                        user_id=user_id,
                    )
                )
                after_point = before_point + bet_amount
            else:
                await EventProducer.create_event(
                    topic='minigame_bet_minus_point',
                    key=uuid_,
                    value=MinigameAdditionPoint(
                        id=uuid_,
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
                    point=after_point,
                    uuid=uuid_,
                    status=MinigameBetStatus.CONFIRMED
                )
            )

            return CoinTossBetRes(
                result=result,
                amount=after_point
            )