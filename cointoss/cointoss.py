import random
from datetime import datetime

from fastapi import status, HTTPException
from py_eureka_client.eureka_client import do_service_async
from sqlmodel.ext.asyncio.session import AsyncSession

from producer import send_message
from db import engine
from minigame.domain.minigame_repo import find_minigame_by_stage_id
from minigame.domain.play import Play


async def coin_toss_bet(headers, stage_id, data):
    user_id = headers['user_id']
    authority = headers['authority']
    bet_amount = data['amount']

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if authority != 'STUDENT':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    async with (AsyncSession(engine) as session):
        async with session.begin():
            # stage_id로 미니게임 조회
            minigame = await find_minigame_by_stage_id(session, stage_id)
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

    return {
        'result': result,
        'amount': after_point
    }