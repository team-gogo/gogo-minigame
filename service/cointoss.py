import json
import random
import time

from fastapi import status, WebSocketException
from py_eureka_client.eureka_client import do_service_async
from sqlmodel.ext.asyncio.session import AsyncSession

from domain.model.coin_toss_result import CoinTossResult
from domain.repository.coin_toss import CoinTossResultRepository
from domain.repository.minigame import MinigameRepository
from domain.repository.ticket import TicketRepository
from presentation.schema.cointoss import CoinTossBetRes
from producer import send_message


class CoinTossService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.minigame_repository = MinigameRepository(session)
        self.coin_toss_result_repository = CoinTossResultRepository(session)
        self.ticket_repository = TicketRepository(session)

    async def bet(self, stage_id, user_id, data):
        async with self.session.begin():
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

            # 티켓 검사
            ticket = await self.ticket_repository.find_by_minigame_id_and_user_id(minigame.minigame_id, user_id)
            if ticket is None or ticket.coin_toss_ticket_amount <= 0:
                raise WebSocketException(code=status.WS_1011_INTERNAL_ERROR, reason='Not enough ticket')

            # 티켓 감소
            ticket.coin_toss_ticket_amount -= 1

            # coin toss 로직
            if result := random.choice([True, False]):
                send_message('increase_point', bet_amount)  # TODO: kafka 토픽, 메시지 변경
                after_point = before_point + bet_amount
            else:
                send_message('decrease_point', bet_amount)  # TODO: kafka 토픽, 메시지 변경
                after_point = before_point - bet_amount

            await self.coin_toss_result_repository.save(
                CoinTossResult(
                    minigame_id=int(minigame.minigame_id),
                    student_id=int(user_id),
                    timestamp=int(time.time()),
                    bet_point=bet_amount,
                    result=result,
                    point=after_point
                )
            )

            return CoinTossBetRes(
                result=result,
                amount=after_point
            ).dict()