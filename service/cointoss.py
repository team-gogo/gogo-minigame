import random
from datetime import datetime

from fastapi import status, HTTPException, WebSocketException
from py_eureka_client.eureka_client import do_service_async
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from domain.model.cointoss import CoinTossBetRes
from producer import send_message
from domain import Play, Minigame


class CoinTossService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def bet(self, stage_id, user_id, data):
        bet_amount = data['amount']

        async with self.session.begin():
            # stage_id로 미니게임 조회
            minigame_select = select(Minigame).where(Minigame.stage_id == stage_id)
            minigame = await self.session.exec(minigame_select)
            if not minigame:
                raise WebSocketException(code=status.WS_1011_INTERNAL_ERROR, reason='Minigame not found')

            # 유저 포인트 정보 가져오기
            response = await do_service_async('gogo-stage', f'/stage/point/{stage_id}?studentId={user_id}')
            if not response:
                raise WebSocketException(code=status.WS_1011_INTERNAL_ERROR, reason='gogo-stage no response')
            before_point = response.json()['point']

            # 포인트 검사
            if bet_amount > before_point:
                raise WebSocketException(code=status.WS_1011_INTERNAL_ERROR, reason='bet amount too high')

            if result := random.choice([True, False]):
                send_message('increase_point', bet_amount)  # TODO: kafka 토픽, 메시지 변경
                after_point = before_point + bet_amount
            else:
                send_message('decrease_point', bet_amount)  # TODO: kafka 토픽, 메시지 변경
                after_point = before_point - bet_amount

            play = Play(
                minigame_id=minigame.id,
                student_id=user_id,
                timestamp=str(datetime.now()),
                bet_point=bet_amount,
                coin_toss_result=result,
                point=after_point
            )
            self.session.add(play)

            return CoinTossBetRes(
                result=result,
                amount=after_point
            )