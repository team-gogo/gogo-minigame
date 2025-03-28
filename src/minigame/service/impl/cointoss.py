import json
import random
import uuid

from fastapi import status, HTTPException
from py_eureka_client.eureka_client import do_service_async
from sqlmodel.ext.asyncio.session import AsyncSession

from src.cointoss.domain.model.coin_toss_result import CoinTossResult
from db import get_session
from event.publisher import EventPublisher
from src.minigame.domain.model.minigame import MinigameBetStatus
from src.minigame.presentation.schema.event import GameType
from src.minigame.service.validation import BetValidationService
from src.cointoss.presentation.schema.cointoss import CoinTossBetReq
from src.minigame.service.bet import MinigameBetService
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
            if minigame is None or not minigame.is_active_coin_toss:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Minigame not found or Not Available')

            await BetValidationService.validate_minigame_status(minigame)

            # Student id 조회
            user_response = await do_service_async('gogo-user', f'/user/student?userId={user_id}')
            if not user_response:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='gogo-stage no response')
            student_id = json.loads(user_response)['studentId']

            # 유저 포인트 정보 가져오기
            response = await do_service_async('gogo-stage', f'/stage/api/point/{stage_id}?studentId={student_id}')
            if not response:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='gogo-stage no response')
            before_point = json.loads(response)['point']

            # 포인트 검사
            if bet_amount > before_point:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='bet amount too high')

            # 티켓 검사
            ticket_amount = await self.ticket_service(await get_session()).get_ticket_amount(user_id=user_id, stage_id=stage_id)
            if ticket_amount is None or ticket_amount.coinToss <= 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not enough ticket')
            ticket = await self.ticket_repository.find_ticket_amount_by_stage_id_and_student_id(stage_id=stage_id, student_id=student_id)

            # 티켓 감소
            ticket.coin_toss_ticket_amount -= 1

            uuid_ = str(uuid.uuid4())

            result = random.choice([True, False])
            earned_point = bet_amount if result else 0
            losted_point = bet_amount if not result else 0

            await EventPublisher.minigame_bet_completed(
                uuid_=uuid_,
                earned_point=earned_point,
                losted_point=losted_point,
                is_win=result,
                student_id=user_id,
                stage_id=stage_id,
                game_type=GameType.COINTOSS
            )

            await self.coin_toss_result_repository.save(
                CoinTossResult(
                    minigame_id=int(minigame.minigame_id),
                    student_id=int(user_id),
                    bet_point=bet_amount,
                    result=result,
                    point=earned_point-losted_point,
                    uuid=uuid_,
                    status=MinigameBetStatus.CONFIRMED
                )
            )

            return CoinTossBetRes(
                result=result,
                amount=data.amount + earned_point - losted_point
            )