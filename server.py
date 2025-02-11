import asyncio

import uvicorn
from fastapi import FastAPI, WebSocketDisconnect
from starlette.websockets import WebSocket
from websockets import ConnectionClosed

from db import create_db
from eureka import init_eureka
from service import coin_toss_bet
from service.plinko import plinko_bet

app = FastAPI()

@app.get('/minigame/health')
async def root():
    return 'GOGO Minigame Service OK'


@app.websocket('/minigame/coin-toss/{stage_id}')
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


@app.websocket('/minigame/plinko/{stage_id}')
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


if __name__ == '__main__':
    try:
        asyncio.run(init_eureka())
        asyncio.run(create_db())
        uvicorn.run(app, host='0.0.0.0', port=8086)
    except Exception as e:
        print(e)
        exit(1)