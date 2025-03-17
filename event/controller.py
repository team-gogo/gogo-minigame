from db import get_session
from event.schema.fast import CreateStageFast
from event.schema.official import CreateStageOfficial
from event.schema.stage import StageConfirmReq
from event.schema.ticket import TicketShopBuyReq
from src.minigame.service.minigame import MinigameService
from src.ticket.service.ticket import TicketService


class EventConsumeController:
    @staticmethod
    async def create_stage_fast(data: CreateStageFast):
        session = await get_session()
        await MinigameService(session).create_minigame_fast(data)

    @staticmethod
    async def create_stage_official(data: CreateStageOfficial):
        session = await get_session()
        await MinigameService(session).create_minigame_official(data)

    @staticmethod
    async def stage_confirm(data: StageConfirmReq):
        session = await get_session()
        await MinigameService(session).confirm_minigame(data)

    @staticmethod
    async def ticket_buy(data: TicketShopBuyReq):
        session = await get_session()
        await TicketService(session).addition_ticket(data)