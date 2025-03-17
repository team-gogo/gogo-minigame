from typing import Annotated

from fastapi import APIRouter, Header, status, Depends
from starlette.websockets import WebSocket, WebSocketDisconnect
from websockets import ConnectionClosed

from src.minigame.factory import MinigameBetServiceFactory, Minigame
from src.yavarwee.presentation.schema.yavarwee import YavarweeBetReq
from authortiy import authority_student

router = APIRouter(prefix='/minigame/yavarwee')


@router.websocket('/{stage_id}')
async def yavarwee(
        stage_id: int,
        websocket: WebSocket,
        request_user_id: Annotated[int, Header()],
        request_user_authority: Annotated[str, Depends(authority_student)]
):

    await websocket.accept()

    while True:
        try:
            data = await websocket.receive_json()
            service = await MinigameBetServiceFactory.create(Minigame.YAVARWEE)
            result = await service.bet(stage_id=stage_id, user_id=request_user_id, data=YavarweeBetReq(**data))
            await websocket.send_json(result.dict())

        except (WebSocketDisconnect, ConnectionClosed):
            break

        except Exception as e:
            await websocket.send_json({'error': str(e)})
            await websocket.close()
            break