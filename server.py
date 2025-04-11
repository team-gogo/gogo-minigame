import asyncio
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from db import create_db
from eureka import init_eureka
from event.consumer import consume
from loki import loki_handler
from middleware import LoggingMiddleware
from src.cointoss.presentation.controller.cointoss import router as coin_toss_router
from src.plinko.presentation.controller.plinko import router as plinko_router
from src.yavarwee.presentation.controller.yavarwee import router as yavarwee_router
from src.ticket.presentation.controller.ticket import router as ticket_router
from src.minigame.presentation.controller.minigame import router as minigame_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(consume())  # 비동기 태스크 실행
    yield

app = FastAPI(lifespan=lifespan)

logger = logging.getLogger('GOGO-MiniGame Logger')
logger.setLevel(logging.INFO)
logger.addHandler(loki_handler)

app.add_middleware(LoggingMiddleware)

app.include_router(coin_toss_router)
app.include_router(plinko_router)
app.include_router(yavarwee_router)
app.include_router(ticket_router)
app.include_router(minigame_router)

@app.get('/minigame/health')
async def root():
    return 'GOGO Minigame Service OK'


if __name__ == '__main__':
    try:
        init_eureka()
        logging.info('init eureka')
        asyncio.run(create_db())
        logging.info('create db')
        uvicorn.run(app, host='0.0.0.0', port=8086, log_level='info', access_log=False)
    except Exception as e:
        print(e)
        exit(1)