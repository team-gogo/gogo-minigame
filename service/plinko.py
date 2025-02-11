import random
from datetime import datetime

from fastapi import HTTPException, status
from py_eureka_client.eureka_client import do_service_async
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from domain import Play, Minigame
from producer import send_message

PLINKO_RISK_VALUE = {
    'LOW': [16, 9, 2, 1.4, 1.4, 1.2, 1.1, 1, 0.5, 1, 1.1, 1.2, 1.4, 1.4, 2, 9, 16],
    'MEDIUM': [110, 41, 10, 5, 3, 1.5, 1, 0.5, 0.3, 0.5, 1, 1.5, 3, 5, 10, 41, 110],
    'HIGH': [1000, 130, 26, 9, 4, 2, 0.2, 0.2, 0.2, 0.2, 0.2, 2, 4, 9, 26, 130, 1000]
}


class PlinkoService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def bet(self, stage_id, user_id, data):
        bet_amount = data['amount']

        async with self.session.begin():
            # stage_id로 미니게임 조회
            minigame_select = select(Minigame).where(Minigame.stage_id == stage_id)
            minigame = await self.session.exec(minigame_select)
            if not minigame:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Minigame not found')

            # 유저 포인트 정보 가져오기
            # TODO: do_service 명세에 맞게 수정 필요
            response = await do_service_async('gogo-stage', f'path?stage_id={stage_id}&user_id={user_id}')
            if not response:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='gogo-stage no response')
            before_point = response.json()['amount']

            # 포인트 검사
            if bet_amount > before_point:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

            # plinko 로직
            row = PLINKO_RISK_VALUE[data.risk]
            move = 0
            path = []
            for _ in range(16):
                path += random.choice([-1, 1])
                move += path
            result = row[8 + (move // 2)]

            # 배팅후 포인트 계산
            plinko_point =+ bet_amount * result
            after_amount = before_point + -bet_amount + plinko_point

            # TODO: 명세에 맞게 변경 필요
            send_message('point', after_amount)

            play = Play(
                minigame_id=minigame.id,
                student_id=user_id,
                timestamp=str(datetime.now()),
                bet_point=bet_amount,
                point=plinko_point,
                plinko_result=result
            )
            self.session.add(play)

            return {
                'amount': after_amount,
                'path': [p for p in path]
            }