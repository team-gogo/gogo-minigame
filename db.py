from sqlalchemy import NullPool, URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from config import DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT
# Register every table in SQLModel.metadata before create_all.
from src.cointoss.domain.model import coin_toss_result
from src.minigame.domain.model import minigame
from src.plinko.domain.model import plinko_result
from src.ticket.domain.model import ticket
from src.yavarwee.domain.model import yavarwee_result

connection_url = URL.create(
    "postgresql+asyncpg",
    username=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

async_engine = create_async_engine(
    connection_url,
    future=True,
    poolclass=NullPool
)

async def create_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async_session = sessionmaker(bind=async_engine, class_=AsyncSession)

    async with async_session() as session:
        return session