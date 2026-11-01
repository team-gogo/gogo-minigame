import asyncio
import logging
from contextlib import asynccontextmanager, suppress

import uvicorn
from fastapi import FastAPI, HTTPException
from sqlalchemy import text

from db import async_engine, create_db
from middleware import LoggingMiddleware
from src.cointoss.presentation.controller.cointoss import router as coin_toss_router
from src.plinko.presentation.controller.plinko import router as plinko_router
from src.yavarwee.presentation.controller.yavarwee import router as yavarwee_router
from src.ticket.presentation.controller.ticket import router as ticket_router
from src.minigame.presentation.controller.minigame import router as minigame_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    from event.consumer import consume
    try:
        await create_db()
        app.state.kafka_ready = asyncio.Event()
        consumer_task = asyncio.create_task(consume(app.state.kafka_ready))
        try:
            yield
        finally:
            consumer_task.cancel()
            with suppress(asyncio.CancelledError):
                await consumer_task
    finally:
        await async_engine.dispose()

app = FastAPI(lifespan=lifespan)

logger = logging.getLogger('GOGO-MiniGame Logger')
logger.setLevel(logging.INFO)

app.add_middleware(LoggingMiddleware)

app.include_router(coin_toss_router)
app.include_router(plinko_router)
app.include_router(yavarwee_router)
app.include_router(ticket_router)
app.include_router(minigame_router)

@app.get('/minigame/health')
async def root():
    return 'GOGO Minigame Service OK'


@app.get('/minigame/health/readiness')
async def readiness():
    if not app.state.kafka_ready.is_set():
        raise HTTPException(status_code=503, detail='Kafka is not ready')
    try:
        async with async_engine.connect() as connection:
            await connection.execute(text('SELECT 1'))
    except Exception as exc:
        raise HTTPException(status_code=503, detail='Database is not ready') from exc
    return {'status': 'UP'}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8086, log_level='info', access_log=False)