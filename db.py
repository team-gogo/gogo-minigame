from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

from config import DB_HOST, DB_NAME, DB_USER, DB_PASS


DB = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'

engine = create_async_engine(DB, echo=True)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)