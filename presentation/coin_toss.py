from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from websockets import ConnectionClosed

from service import coin_toss_bet

router = APIRouter(prefix='/minigame/coin-toss')


@router.websocket('/{stage_id}')
async def coin_toss(websocket: WebSocket, stage_id: int):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_json()
            result = await coin_toss_bet(headers=websocket.headers, stage_id=stage_id, data=data)
            await websocket.send_json(result)
        except (WebSocketDisconnect, ConnectionClosed):
            break
        except Exception as e:
            await websocket.send_json({'error': str(e)})
            await websocket.close()
            break