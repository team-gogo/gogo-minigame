import asyncio

import uvicorn
from fastapi import FastAPI

from db import create_db
from eureka import init_eureka
from presentation.cointoss import router as coin_toss_router
from presentation.plinko import router as plinko_router
from presentation.yavarwee import router as yavarwee_router
from presentation.ticket import router as ticket_router

app = FastAPI()


@app.get('/minigame/health')
async def root():
    return 'GOGO Minigame Service OK'


app.include_router(coin_toss_router)
app.include_router(plinko_router)
app.include_router(yavarwee_router)
app.include_router(ticket_router)

if __name__ == '__main__':
    try:
        init_eureka()
        asyncio.run(create_db())
        uvicorn.run(app, host='0.0.0.0', port=8086)
    except Exception as e:
        print(e)
        exit(1)