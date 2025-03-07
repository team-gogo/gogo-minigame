from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.minigame.domain.model.minigame import Minigame


class MinigameRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_stage_id(self, stage_id) -> Minigame:
        statement = select(Minigame).where(Minigame.stage_id == stage_id)
        result = await self.session.exec(statement)
        return result.first()
