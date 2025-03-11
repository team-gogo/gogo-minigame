import base64
import json
import time

from fastapi import WebSocketException, status
from py_eureka_client.eureka_client import do_service_async
from sqlmodel.ext.asyncio.session import AsyncSession

from event.producer import EventProducer
from src.minigame.service.validation import BetValidationService
from src.minigame.presentation.schema.event import MinigameAdditionPoint
from src.minigame.service.bet import MinigameBetService
from src.yavarwee.domain.model.yavarwee_result import YavarweeResult
from src.yavarwee.domain.repository.yavarwee import YavarweeResultRepository
from src.minigame.domain.repository.minigame import MinigameRepository
from src.ticket.domain.repository.ticket import TicketRepository
from src.yavarwee.presentation.schema.yavarwee import YavarweeBetReq, YavarweeBetRes
from config import YAVARWEE_SECRET

YAVARWEE_ROUND_VALUE = [1.1, 1.3, 1.5, 2, 5]


class YavarweeMinigameBetServiceImpl(MinigameBetService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.minigame_repository = MinigameRepository(session)
        self.yavarwee_repository = YavarweeResultRepository(session)
        self.ticket_repository = TicketRepository(session)

    async def bet(self, stage_id, user_id, data: YavarweeBetReq):
        async with (self.session.begin()):
            bet_amount = data.amount

            await BetValidationService.validate_proof(uuid=data.uuid, amount=data.amount, round_=data.round)

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

            # UUID 검사
            if await self.yavarwee_repository.find_by_uuid(data.uuid):
                raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason='uuid already exists')

            # 티켓 검사
            ticket = await self.ticket_repository.find_by_minigame_id_and_user_id_for_update(minigame.minigame_id, user_id)
            if ticket is None or ticket.yavarwee_ticket_amount <= 0:
                raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason='Not enough ticket')

            # 티켓 감소
            ticket.plinko_ticket_amount -= 1

            yavarwee_point = bet_amount * YAVARWEE_ROUND_VALUE[data.round - 1] - bet_amount

            await EventProducer.create_event(
                'minigame_bet_addition_point',
                MinigameAdditionPoint(
                    point=yavarwee_point,
                    user_id=user_id,
                )
            )


            await self.yavarwee_repository.save(
                YavarweeResult(
                    minigame_id=minigame.minigame_id,
                    student_id=user_id,
                    timestamp=int(time.time()),
                    bet_point=bet_amount,
                    yavarwee_stage=data.round,
                    point=yavarwee_point,
                    uuid=data.uuid,
                )
            )

        after_point = before_point + yavarwee_point

        return YavarweeBetRes(
            amount=after_point
        )