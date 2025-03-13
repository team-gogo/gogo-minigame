from db import get_session
from event.schema.fast import CreateStageFast
from event.schema.stage import StageConfirmReq
from event.schema.ticket import TicketShopBuyReq
from src.minigame.presentation.schema.minigame import MinigameCreateReq
from src.minigame.service.minigame import MinigameService
from src.ticket.service.ticket import TicketService


class EventConsumeController:
    @staticmethod
    async def create_stage_fast(data: CreateStageFast):
        session = await get_session()
        await MinigameService(session).create_minigame(
            MinigameCreateReq(
                stage_id=data.stageId,
                is_active_coin_toss=data.miniGame.isCoinTossActive,
                coin_toss_max_betting_point=data.miniGame.coinTossMaxBettingPoint,
                coin_toss_min_betting_point=data.miniGame.coinTossMinBettingPoint
            )
        )

    @staticmethod
    async def create_stage_official(data):
        session = await get_session()
        await MinigameService(session).create_minigame(
            MinigameCreateReq(
                stage_id=data.stageId,
                is_active_plinko= data.miniGame.isPlinkoActive,
                is_active_yavarwee=data.miniGame.isYavarweeActive,
                is_active_coin_toss=data.miniGame.isCoinTossActive
            )
        )

    @staticmethod
    async def stage_confirm(data: StageConfirmReq):
        session = await get_session()
        await MinigameService(session).confirm_minigame(data.stageId)

    @staticmethod
    async def ticket_buy(data: TicketShopBuyReq):
        session = await get_session()
        await TicketService(session).addition_ticket(
            user_id=data.studentId,
            stage_id=data.stageId,
            ticket_amount=data.purchaseQuantity,
            game=data.ticketType
        )