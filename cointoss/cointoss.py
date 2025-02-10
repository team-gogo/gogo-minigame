import random
from datetime import datetime

from fastapi import status, HTTPException
from py_eureka_client.eureka_client import do_service_async
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from producer import send_message
from db import engine
from model.play import Play
from model.minigame import Minigame


async def bet(headers, stage_id, data):
    user_id = headers['user_id']
    authority = headers['authority']
    bet_amount = data['amount']

    if not user_id:
        raise HTTPException(code=status.HTTP_401_UNAUTHORIZED)

    if authority != 'STUDENT':
        raise HTTPException(code=status.HTTP_403_FORBIDDEN)

    async with (AsyncSession(engine) as session):
        # stage id로 minigame 조회
        minigame_select = select(Minigame).where(Minigame.stage_id == stage_id)
        minigame = await session.exec(minigame_select)
        if not minigame:
            raise HTTPException(code=status.HTTP_404_NOT_FOUND, detail='Minigame not found')

        # 유저 포인트 정보 가져오기
        # TODO: do_service 명세에 맞게 수정 필요
        response = await do_service_async('gogo-stage', f'path?stage_id={stage_id}&user_id={user_id}')
        if not response:
            raise HTTPException(code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='gogo-stage no response')
        before_point = response.json()['amount']

        # 포인트 검사
        if bet_amount > before_point:
            raise HTTPException(code=status.HTTP_400_BAD_REQUEST)

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
            point=after_point
        )

        session.add(play)
        await session.commit()

    return {
        'result': result,
        'amount': after_point
    }