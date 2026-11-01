import asyncio
import os

import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

pytestmark = pytest.mark.skipif(
    os.environ.get('RUN_POSTGRES_TESTS') != '1',
    reason='Set RUN_POSTGRES_TESTS=1 with an isolated PostgreSQL database',
)


def test_postgres_schema_and_stage_uniqueness():
    from db import async_engine, create_db
    from src.minigame.domain.model.minigame import Minigame, MinigameStatus

    async def verify():
        await create_db()
        await create_db()  # Repeat startup must not drop persisted schema.
        async with async_engine.connect() as conn:
            tables = await conn.run_sync(lambda sync: set(inspect(sync).get_table_names()))
            assert set(SQLModel.metadata.tables).issubset(tables)
        async with AsyncSession(async_engine) as session:
            game = Minigame(stage_id=9223372036854770000)
            session.add(game)
            await session.flush()
            assert game.minigame_id is not None
            result = await session.exec(select(Minigame).where(Minigame.stage_id == game.stage_id))
            assert result.one().status == MinigameStatus.PENDING
            session.add(Minigame(stage_id=game.stage_id))
            with pytest.raises(IntegrityError):
                await session.flush()
            await session.rollback()
        await async_engine.dispose()

    asyncio.run(verify())
