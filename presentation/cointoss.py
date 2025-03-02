from typing import Annotated

from django.contrib.auth import authenticate
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, status, Depends
from fastapi.params import Header
from sqlmodel.ext.asyncio.session import AsyncSession
from websockets import ConnectionClosed

from db import get_session
from service.cointoss import CoinTossService

router = APIRouter(prefix='/minigame/coin-toss')


@router.websocket('/{stage_id}')
async def coin_toss(
        stage_id: int,
        websocket: WebSocket,
        user_id: Annotated[int, Header()],
        authority: Annotated[str, Header()],
        session: Annotated[AsyncSession, Depends(get_session)],
):

    if authority != 'STUDENT':
        raise websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    await websocket.accept()

    while True:
        try:
            data = await websocket.receive_json()
            result = await CoinTossService(session).bet(stage_id=stage_id, user_id=user_id, data=data)
            await websocket.send_json(result)

        except (WebSocketDisconnect, ConnectionClosed):
            break

        except Exception as e:
            await websocket.send_json({'error': str(e)})
            await websocket.close()
            break