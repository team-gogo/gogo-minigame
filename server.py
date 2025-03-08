import asyncio

import uvicorn
from fastapi import FastAPI

from db import create_db
from eureka import init_eureka
from src.cointoss.presentation.controller.cointoss import router as coin_toss_router
from src.plinko.presentation.controller.plinko import router as plinko_router
from src.yavarwee.presentation.controller.yavarwee import router as yavarwee_router
from src.ticket.presentation.controller.ticket import router as ticket_router
from src.minigame.presentation.controller.minigame import router as minigame_router

app = FastAPI()


@app.get('/minigame/health')
async def root():
    return 'GOGO Minigame Service OK'


app.include_router(coin_toss_router)
app.include_router(plinko_router)
app.include_router(yavarwee_router)
app.include_router(ticket_router)
app.include_router(minigame_router)

if __name__ == '__main__':
    try:
        init_eureka()
        asyncio.run(create_db())
        uvicorn.run(app, host='0.0.0.0', port=8086)
    except Exception as e:
        print(e)
        exit(1)