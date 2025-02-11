import uvicorn
from fastapi import FastAPI
from starlette.websockets import WebSocket

from db import create_db
from eureka import init_eureka
from service import coin_toss_bet

app = FastAPI()

@app.get('/minigame/health')
async def root():
    return 'GOGO Minigame Service OK'


@app.websocket('/minigame/coin-toss/{stage_id}')
async def coin_toss(websocket: WebSocket, stage_id: int):
    headers = websocket.headers
    await websocket.accept()

    while True:
        data = await websocket.receive_json()

        try:
            result = await coin_toss_bet(headers=headers, stage_id=stage_id, data=data)
        except Exception as e:
            result = {'error': str(e)}

        await websocket.send_json(result)


@app.websocket('/minigame/plinko/{stage_id}')
async def plinko(websocket: WebSocket, stage_id: int):
    headers = websocket.headers
    await websocket.accept()

    while True:
        data = await websocket.receive_json()

        try:
            result = await coin_toss_bet(headers=headers, stage_id=stage_id, data=data)
            await websocket.send_json(result)
        except Exception as e:
            result = {'error': str(e)}

        await websocket.send_json(result)


if __name__ == '__main__':
    try:
        create_db()
        init_eureka()
        uvicorn.run(app, host='0.0.0.0', port=8086)
    except Exception as e:
        exit(1)
