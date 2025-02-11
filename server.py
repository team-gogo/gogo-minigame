import asyncio

import uvicorn
from fastapi import FastAPI
from starlette.websockets import WebSocket

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
        except Exception as e:
            result = {'error': str(e)}
        finally:
            await websocket.send_json(result)


@app.websocket('/minigame/plinko/{stage_id}')
async def plinko(websocket: WebSocket, stage_id: int):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_json()
            result = await plinko_bet(headers=websocket.headers, stage_id=stage_id, data=data)
            await websocket.send_json(result)
        except Exception as e:
            result = {'error': str(e)}
        finally:
            await websocket.send_json(result)


if __name__ == '__main__':
    try:
        init_eureka()
        create_db()
        uvicorn.run(app, host='0.0.0.0', port=8086)
    except Exception as e:
        print(e)
        exit(1)