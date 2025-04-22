from sqlalchemy import NullPool, URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from config import DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT

connection_url = URL.create(
    "mysql+aiomysql",
    username=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

async_engine = create_async_engine(
    connection_url,
    future=True,
    echo=True,
    poolclass=NullPool
)

async def create_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async_session = sessionmaker(bind=async_engine, class_=AsyncSession)

    async with async_session() as session:
        return session