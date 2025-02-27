import json
import random
import time

from fastapi import status
from py_eureka_client.eureka_client import do_service_async
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.exceptions import WebSocketException

from domain.model.plinko_result import PlinkoResult
from domain.repository.minigame import MinigameRepository
from domain.repository.plinko import PlinkoResultRepository
from presentation.schema.plinko import PlinkoBetRes
from producer import send_message

PLINKO_RISK_VALUE = {
    'LOW': [16, 9, 2, 1.4, 1.4, 1.2, 1.1, 1, 0.5, 1, 1.1, 1.2, 1.4, 1.4, 2, 9, 16],
    'MEDIUM': [110, 41, 10, 5, 3, 1.5, 1, 0.5, 0.3, 0.5, 1, 1.5, 3, 5, 10, 41, 110],
    'HIGH': [1000, 130, 26, 9, 4, 2, 0.2, 0.2, 0.2, 0.2, 0.2, 2, 4, 9, 26, 130, 1000]
}


class PlinkoService:
    def __init__(self, session: AsyncSession):
        self.minigame_repository = MinigameRepository(session)
        self.plinko_result_repository = PlinkoResultRepository(session)

    async def bet(self, stage_id, user_id, data):
        bet_amount = data['amount']

        # stage_id로 미니게임 조회
        minigame = await self.minigame_repository.find_by_stage_id(stage_id)
        if not minigame:
            raise WebSocketException(code=status.WS_1011_INTERNAL_ERROR, reason='Minigame not found')

        # 유저 포인트 정보 가져오기
        response = await do_service_async('gogo-stage', f'/stage/api/point/{stage_id}?studentId={user_id}')
        if not response:
            raise WebSocketException(code=status.WS_1011_INTERNAL_ERROR, reason='gogo-stage no response')
        before_point = json.loads(response)['point']

        # 포인트 검사
        if bet_amount > before_point:
            raise WebSocketException(code=status.WS_1011_INTERNAL_ERROR, reason='bet amount too high')

        # plinko 로직
        row = PLINKO_RISK_VALUE[data['risk']]
        move = 0
        path = []
        for i in range(16):
            step = random.choice([-1, 1])
            path.append(step)
            move += step
        result = row[8 + (move // 2)]

        # 배팅후 포인트 계산
        plinko_point = bet_amount * result
        after_amount = before_point + -bet_amount + plinko_point

        # TODO: 명세에 맞게 변경 필요
        send_message('point', after_amount)

        await self.plinko_result_repository.save(
            PlinkoResult(
                minigame_id=minigame.minigame_id,
                student_id=user_id,
                timestamp=int(time.time()),
                bet_point=bet_amount,
                point=plinko_point,
                result=result
            )
        )

        return PlinkoBetRes(
            amount=bet_amount,
            path=['L' if p==-1 else 'R' for p in path],
        ).dict()