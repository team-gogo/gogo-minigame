from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException

from src.minigame.domain.model.minigame import Minigame, MinigameStatus
from src.minigame.presentation.schema.minigame import MinigameCreateReq
from src.minigame.domain.repository.minigame import MinigameRepository
from src.minigame.presentation.schema.minigame import GetActiveMinigameRes


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

    async def create_minigame(self, data: MinigameCreateReq):
        async with self.session.begin():
            return await self.minigame_repository.save(
                Minigame(
                    stage_id=data.stage_id,
                    is_active_plinko=data.is_active_plinko,
                    is_active_coin_toss=data.is_active_coin_toss,
                    is_active_yavarwee=data.is_active_yavarwee,
                    coin_toss_max_betting_point=data.coin_toss_max_betting_point,
                    coin_toss_min_betting_point=data.coin_toss_min_betting_point,
                    yavarwee_max_betting_point=data.yavarwee_max_betting_point,
                    yavarwee_min_betting_point=data.yavarwee_min_betting_point,
                    plinko_max_betting_point=data.plinko_max_betting_point,
                    plinko_min_betting_point=data.plinko_min_betting_point,
                )
            )

    async def confirm_minigame(self, stage_id):
        async with self.session.begin():
            minigame = await self.minigame_repository.find_by_stage_id(stage_id)
            if minigame is None:
                raise HTTPException(status_code=404, detail="Minigame not found")
            minigame.status = MinigameStatus.ACTIVE