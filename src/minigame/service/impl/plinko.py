import json
import random
import time

from fastapi import status
from py_eureka_client.eureka_client import do_service_async
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.exceptions import WebSocketException

from src.minigame.presentation.schema.event import MinigameAdditionPoint
from src.plinko.presentation.schema.plinko import PlinkoBetReq
from src.minigame.domain.repository.minigame import MinigameRepository
from src.plinko.domain.repository.plinko import PlinkoResultRepository
from src.plinko.domain.model.plinko_result import PlinkoResult
from src.plinko.presentation.schema.plinko import PlinkoBetRes
from src.minigame.service.bet import MinigameBetService
from event.producer import EventProducer
from src.ticket.domain.repository.ticket import TicketRepository

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

    async def bet(self, stage_id: int, user_id: int, data: PlinkoBetReq):
        async with self.session.begin():
            bet_amount = data.amount

            # stage_id로 미니게임 조회
            minigame = await self.minigame_repository.find_by_stage_id(stage_id)
            if not minigame.is_active_plinko:
                raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason='Minigame not found')

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
            if ticket is None or ticket.plinko_ticket_amount <= 0:
                raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason='Not enough ticket')

            # 티켓 감소
            ticket.plinko_ticket_amount -= 1

            # plinko 로직
            row = PLINKO_RISK_VALUE[data.risk.value]
            move = 0
            path = []
            for i in range(16):
                step = random.choice([-1, 1])
                path.append(step)
                move += step
            result = row[8 + (move // 2)]

            # 배팅후 포인트 계산
            plinko_point = bet_amount * result

            # Event 발급
            addition_point = bet_amount * result - bet_amount
            if addition_point > 0:
                await EventProducer.create_event(
                    'minigame_bet_addition_point',
                    MinigameAdditionPoint(
                        point=addition_point,
                        user_id=user_id,
                    )
                )
            else:
                await EventProducer.create_event(
                    'minigame_bet_minus_point',
                    MinigameAdditionPoint(
                        point=-addition_point,
                        user_id=user_id,
                    )
                )

            await self.plinko_result_repository.save(
                PlinkoResult(
                    minigame_id=int(minigame.minigame_id),
                    student_id=int(user_id),
                    timestamp=int(time.time()),
                    bet_point=bet_amount,
                    point=plinko_point,
                    result=result
                )
            )

            return PlinkoBetRes(
                amount=result,
                path=['L' if p==-1 else 'R' for p in path],
            )