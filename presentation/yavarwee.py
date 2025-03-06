from typing import Annotated

from fastapi import APIRouter, Header, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect
from websockets import ConnectionClosed

from db import get_session
from presentation.schema.yavarwee import YavarweeBetReq
from service.yavarwee import YavarweeService

router = APIRouter(prefix='/minigame/yavarwee')


@router.websocket('/{stage_id}')
async def yavarwee(
        stage_id: int,
        websocket: WebSocket,
        request_user_id: Annotated[int, Header()],
        authority: Annotated[str, Header()],
        session: Annotated[AsyncSession, Depends(get_session)],
):
    if authority != 'STUDENT':
        raise websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    await websocket.accept()

    while True:
        try:
            data = await websocket.receive_json()
            result = await YavarweeService(session).bet(stage_id=stage_id, user_id=request_user_id, data=YavarweeBetReq(**data))
            await websocket.send_json(result)

        except (WebSocketDisconnect, ConnectionClosed):
            break

        except Exception as e:
            await websocket.send_json({'error': str(e)})
            await websocket.close()
            break