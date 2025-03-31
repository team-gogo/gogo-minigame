from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status

from event.schema.fast import CreateStageFast
from event.schema.official import CreateStageOfficial
from src.minigame.domain.model.minigame import Minigame, MinigameStatus
from src.minigame.domain.repository.minigame import MinigameRepository
from src.minigame.presentation.schema.minigame import GetActiveMinigameRes
from src.ticket.domain.repository.ticket import TicketRepository


class MinigameService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.minigame_repository = MinigameRepository(session)
        self.ticket_repository = TicketRepository(session)

    async def get_active_minigame(self, stage_id):
        async with self.session.begin():
            minigame = await self.minigame_repository.find_by_stage_id(stage_id)
            if minigame is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Minigame not found")
            return GetActiveMinigameRes(
                isPlinkoActive=minigame.is_active_plinko,
                isCoinTossActive=minigame.is_active_coin_toss,
                isYavarweeActive=minigame.is_active_yavarwee,
            )

    async def create_minigame_fast(self, data: CreateStageFast):
        async with self.session.begin():
            # 미니게임 스테이지 생성
            await self.minigame_repository.save(
                Minigame(
                    stage_id=data.stageId,
                    is_active_coin_toss=data.miniGame.isCoinTossActive,
                    coin_toss_max_betting_point=data.miniGame.coinTossMaxBettingPoint,
                    coin_toss_min_betting_point=data.miniGame.coinTossMinBettingPoint,
                    coin_toss_default_ticket_amount=data.miniGame.coinTossInitialTicketCount,
                    coin_toss_initial_ticket_count=data.miniGame.coinTossInitialTicketCount,
                )
            )

    async def create_minigame_official(self, data: CreateStageOfficial):
        async with self.session.begin():
            return await self.minigame_repository.save(
                Minigame(
                    stage_id=data.stageId,

                    is_active_coin_toss=data.miniGame.coinToss.isActive,
                    is_active_plinko=data.miniGame.plinko.isActive,
                    is_active_yavarwee=data.miniGame.yavarwee.isActive,

                    coin_toss_default_ticket_amount=data.miniGame.coinToss.initialTicketCount,
                    yavarwee_default_ticket_amount=data.miniGame.yavarwee.initialTicketCount,
                    plinko_default_ticket_amount=data.miniGame.plinko.initialTicketCount,

                    coin_toss_max_betting_point=data.miniGame.coinToss.maxBettingPoint,
                    coin_toss_min_betting_point=data.miniGame.coinToss.minBettingPoint,
                    coin_toss_initial_ticket_count=data.miniGame.coinToss.initialTicketCount,

                    yavarwee_max_betting_point=data.miniGame.yavarwee.maxBettingPoint,
                    yavarwee_min_betting_point=data.miniGame.yavarwee.minBettingPoint,
                    yavarwee_initial_ticket_count=data.miniGame.yavarwee.initialTicketCount,

                    plinko_max_betting_point=data.miniGame.plinko.maxBettingPoint,
                    plinko_min_betting_point=data.miniGame.plinko.minBettingPoint,
                    plinko_initial_ticket_count=data.miniGame.plinko.initialTicketCount,
                )
            )

    async def confirm_minigame(self, stage_id):
        async with self.session.begin():
            minigame = await self.minigame_repository.find_by_stage_id(stage_id)
            if minigame is None:
                raise HTTPException(status_code=404, detail="Minigame not found")
            minigame.status = MinigameStatus.ACTIVE