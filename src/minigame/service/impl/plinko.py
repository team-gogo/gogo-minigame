import json
import random
import time
import uuid

from fastapi import status, HTTPException
from py_eureka_client.eureka_client import do_service_async
from sqlmodel.ext.asyncio.session import AsyncSession

from db import get_session
from event.publisher import EventPublisher
from src.minigame.presentation.schema.event import GameType
from src.minigame.domain.model.minigame import MinigameBetStatus
from src.minigame.service.validation import BetValidationService
from src.plinko.presentation.schema.plinko import PlinkoBetReq
from src.minigame.domain.repository.minigame import MinigameRepository
from src.plinko.domain.repository.plinko import PlinkoResultRepository
from src.plinko.domain.model.plinko_result import PlinkoResult
from src.plinko.presentation.schema.plinko import PlinkoBetRes
from src.minigame.service.bet import MinigameBetService
from src.ticket.domain.repository.ticket import TicketRepository
from src.ticket.service.ticket import TicketService

PLINKO_RISK_VALUE = {
    'LOW': [16, 9, 2, 1.4, 1.4, 1.2, 1.1, 1, 0.5, 1, 1.1, 1.2, 1.4, 1.4, 2, 9, 16],
    'MEDIUM': [110, 41, 10, 5, 3, 1.5, 1, 0.5, 0.3, 0.5, 1, 1.5, 3, 5, 10, 41, 110],
    'HIGH': [1000, 130, 26, 9, 4, 2, 0.2, 0.2, 0.2, 0.2, 0.2, 2, 4, 9, 26, 130, 1000]
}


class PlinkoMinigameBetServiceImpl(MinigameBetService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.minigame_repository = MinigameRepository(session)
        self.plinko_result_repository = PlinkoResultRepository(session)
        self.ticket_repository = TicketRepository(session)
        self.ticket_service = TicketService

    async def bet(self, stage_id: int, user_id: int, data: PlinkoBetReq):
        async with self.session.begin():
            bet_amount = data.amount

            # stage_id로 미니게임 조회
            minigame = await self.minigame_repository.find_by_stage_id(stage_id)
            if minigame is None or not minigame.is_active_plinko:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Minigame not found or Not Available')

            await BetValidationService.validate_minigame_status(minigame)

            # Student id 조회
            user_response = await do_service_async('gogo-user', f'/user/student?userId={user_id}')
            if not user_response:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='gogo-stage no response')
            student_id = json.loads(user_response)['studentId']

            await BetValidationService.is_student_participate_in_stage(stage_id=stage_id, student_id=student_id)

            # 유저 포인트 정보 가져오기
            response = await do_service_async('gogo-stage', f'/stage/api/point/{stage_id}?studentId={student_id}')
            if not response:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='gogo-stage no response')
            before_point = json.loads(response)['point']

            # 최대 최소 베팅 포인트 검사
            if bet_amount < minigame.plinko_min_betting_point or bet_amount > minigame.plinko_max_betting_point:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='bet amount out of range')

            # 포인트 검사
            if bet_amount > before_point:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='bet amount too high')

            # 티켓 검사
            ticket_amount = await self.ticket_service(await get_session()).get_ticket_amount(user_id=user_id, stage_id=stage_id)
            if ticket_amount is None or ticket_amount.plinko <= 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not enough ticket')
            ticket = await self.ticket_repository.find_ticket_amount_by_stage_id_and_student_id(stage_id=stage_id, student_id=student_id)

            # 티켓 감소
            ticket.plinko_ticket_amount -= 1
            uuid_ = str(uuid.uuid4())

            # plinko 로직
            row = PLINKO_RISK_VALUE[data.risk.value]
            move = 0
            path = []
            for i in range(16):
                step = random.choice([-1, 1])
                path.append(step)
                move += step
            index_ = 8 + (move // 2)
            result = row[index_]

            # 배팅후 포인트 계산
            plinko_point = int(bet_amount * result)
            changed_point = int(plinko_point - bet_amount)

            earned_point = int(changed_point if changed_point > 0 else 0)
            losted_point = int((changed_point if changed_point < 0 else 0) * -1)
            is_win = True if earned_point != 0 else False

            await EventPublisher.minigame_bet_completed(
                uuid_=uuid_,
                earned_point=earned_point,
                losted_point=losted_point,
                is_win=is_win,
                student_id=int(student_id),
                stage_id=stage_id,
                game_type=GameType.PLINKO.value
            )

            await self.plinko_result_repository.save(
                PlinkoResult(
                    minigame_id=int(minigame.minigame_id),
                    student_id=int(student_id),
                    bet_point=bet_amount,
                    point=earned_point-losted_point,
                    result=result,
                    uuid=uuid_,
                    status=MinigameBetStatus.CONFIRMED
                )
            )

            return PlinkoBetRes(
                amount=bet_amount + earned_point - losted_point,
                path=['L' if p==-1 else 'R' for p in path],
                multi=index_
            )
