from sqlmodel.ext.asyncio.session import AsyncSession

from domain.repository.minigame import MinigameRepository
from presentation.schema.minigame import GetActiveMinigameRes


class MinigameService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.minigame_repository = MinigameRepository(session)

    async def get_active_minigame(self, stage_id):
        async with self.session.begin():
            minigame = await self.minigame_repository.find_by_stage_id(stage_id)
            return GetActiveMinigameRes(
                isPlinkoActive=minigame.is_active_plinko,
                isCoinTossActive=minigame.is_active_coin_toss,
                isYavarweeActive=minigame.is_active_yavarwee,
            )