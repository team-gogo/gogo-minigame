from fastapi import APIRouter, WebSocketDisconnect, WebSocket
from websockets import ConnectionClosed

from service.plinko import plinko_bet

router = APIRouter(prefix='/minigame/plinko')


@router.websocket('/{stage_id}')
async def plinko(websocket: WebSocket, stage_id: int):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_json()
            result = await plinko_bet(headers=websocket.headers, stage_id=stage_id, data=data)
            await websocket.send_json(result)
        except (WebSocketDisconnect, ConnectionClosed):
            break
        except Exception as e:
            await websocket.send_json({'error': str(e)})
            await websocket.close()
            break