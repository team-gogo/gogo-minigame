import json
import time

from fastapi import status, HTTPException
from py_eureka_client.eureka_client import do_service_async
from sqlmodel.ext.asyncio.session import AsyncSession

from db import get_session
from event.publisher import EventPublisher
from src.minigame.presentation.schema.event import GameType
from src.minigame.domain.model.minigame import MinigameBetStatus
from src.minigame.service.validation import BetValidationService
from src.minigame.service.bet import MinigameBetService
from src.yavarwee.domain.model.yavarwee_result import YavarweeResult
from src.yavarwee.domain.repository.yavarwee import YavarweeResultRepository
from src.minigame.domain.repository.minigame import MinigameRepository
from src.ticket.domain.repository.ticket import TicketRepository
from src.yavarwee.presentation.schema.yavarwee import YavarweeBetReq, YavarweeBetRes
from src.ticket.service.ticket import TicketService

YAVARWEE_ROUND_VALUE = [1.1, 1.3, 1.5, 2, 5]


class YavarweeMinigameBetServiceImpl(MinigameBetService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.minigame_repository = MinigameRepository(session)
        self.yavarwee_repository = YavarweeResultRepository(session)
        self.ticket_repository = TicketRepository(session)
        self.ticket_service = TicketService

    async def bet(self, stage_id, user_id, data: YavarweeBetReq):
        async with (self.session.begin()):
            bet_amount = data.amount

            await BetValidationService.validate_proof(uuid=data.uuid, amount=data.amount, round_=data.round, proof=data.proof)

            # stage_id로 미니게임 조회
            minigame = await self.minigame_repository.find_by_stage_id(stage_id)
            if not minigame.is_active_yavarwee:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Minigame not found')

            await BetValidationService.validate_minigame_status(minigame)

            # 유저 포인트 정보 가져오기
            response = await do_service_async('gogo-stage', f'/stage/api/point/{stage_id}?studentId={user_id}')
            if not response:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='gogo-stage no response')
            before_point = json.loads(response)['point']

            # 포인트 검사
            if bet_amount > before_point:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='bet amount too high')

            # UUID 검사
            if await self.yavarwee_repository.find_by_uuid(str(data.uuid)):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='uuid already exists')

            # 티켓 검사
            ticket_amount = await self.ticket_service(await get_session()).get_ticket_amount(user_id=user_id, stage_id=stage_id)
            if ticket_amount is None or ticket_amount.yavarwee <= 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not enough ticket')
            ticket = await self.ticket_repository.find_ticket_amount_by_stage_id_and_user_id(stage_id=stage_id, user_id=user_id)

            # 티켓 감소
            ticket.plinko_ticket_amount -= 1

            earned_point = bet_amount * YAVARWEE_ROUND_VALUE[data.round - 1] - bet_amount

            await EventPublisher.minigame_bet_completed(
                uuid_=data.uuid,
                earned_point=earned_point,
                losted_point=0,
                is_win=True,
                student_id=user_id,
                stage_id=stage_id,
                game_type=GameType.YAVARWEE.value
            )

            await self.yavarwee_repository.save(
                YavarweeResult(
                    minigame_id=minigame.minigame_id,
                    student_id=user_id,
                    timestamp=int(time.time()),
                    bet_point=bet_amount,
                    yavarwee_stage=data.round,
                    point=earned_point,
                    uuid=str(data.uuid),
                    status=MinigameBetStatus.CONFIRMED
                )
            )

        after_point = before_point + earned_point

        return YavarweeBetRes(
            amount=after_point
        )