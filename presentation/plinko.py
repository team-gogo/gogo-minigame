from fastapi import APIRouter, WebSocketDisconnect, WebSocket, HTTPException, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from websockets import ConnectionClosed

from service.plinko import PlinkoService
from db import get_session

router = APIRouter(prefix='/minigame/plinko')


@router.websocket('/{stage_id}')
async def plinko(
        stage_id: int,
        websocket: WebSocket,
        session: AsyncSession = Depends(get_session)
):
    headers = websocket.headers

    user_id = headers['user_id']
    authority = headers['authority']

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if authority != 'STUDENT':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    await websocket.accept()

    while True:
        try:
            data = await websocket.receive_json()
            result = await PlinkoService(session).bet(stage_id=stage_id, user_id=user_id, data=data)
            await websocket.send_json(result)

        except (WebSocketDisconnect, ConnectionClosed):
            break

        except Exception as e:
            await websocket.send_json({'error': str(e)})
            await websocket.close()
            break