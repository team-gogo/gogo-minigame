from typing import Annotated

from fastapi import APIRouter, WebSocketDisconnect, WebSocket, status, Depends
from fastapi.params import Header
from websockets import ConnectionClosed

from authortiy import authority_student
from src.plinko.presentation.schema.plinko import PlinkoBetReq
from src.minigame.factory import MinigameBetServiceFactory, Minigame

router = APIRouter(prefix='/minigame/plinko')


@router.websocket('/{stage_id}')
async def plinko(
        stage_id: int,
        websocket: WebSocket,
        request_user_id: Annotated[int, Header()],
        authority: Annotated[str, Depends(authority_student)]
):
    await websocket.accept()

    while True:
        try:
            data = await websocket.receive_json()
            service = await MinigameBetServiceFactory.create(Minigame.PLINKO)
            result = await service.bet(stage_id=stage_id, user_id=request_user_id, data=PlinkoBetReq(**data))
            await websocket.send_json(result.dict())

        except (WebSocketDisconnect, ConnectionClosed):
            break

        except Exception as e:
            await websocket.send_json({'error': str(e)})
            await websocket.close()
            break