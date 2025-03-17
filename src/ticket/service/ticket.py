from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession

from event.schema.ticket import TicketType, TicketShopBuyReq
from src.minigame.domain.repository.minigame import MinigameRepository
from src.ticket.domain.repository.ticket import TicketRepository
from src.ticket.presentation.schema.ticket import GetTicketAmountRes
from src.ticket.domain.model.ticket import Ticket
from event.producer import EventProducer

class TicketEventFail(BaseModel):
    id: str
    stageId: int
    studentId: int
    shopMiniGameId: int
    ticketType: str
    shopReceiptId: int
    ticketPrice: int
    purchaseQuantity: int


class TicketService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.ticket_repository = TicketRepository(session)
        self.minigame_repository = MinigameRepository(session)

    async def get_ticket_amount(self, user_id, stage_id):
        async with self.session.begin():
            ticket = await self.ticket_repository.find_ticket_amount_by_stage_id_and_user_id(stage_id=stage_id, user_id=user_id)
            if ticket is None:
                minigame = await self.minigame_repository.find_by_stage_id(stage_id)
                await self.ticket_repository.save(
                    Ticket(
                        minigame_id=minigame.minigame_id,
                        user_id=user_id,
                        coin_toss_ticket_amount=minigame.coin_toss_default_ticket_amount,
                        yavarwee_ticket_amount=minigame.yavarwee_default_ticket_amount,
                        plinko_ticket_amount=minigame.plinko_default_ticket_amount
                    )
                )
                await self.session.flush()
                ticket = await self.ticket_repository.find_ticket_amount_by_stage_id_and_user_id(stage_id=stage_id, user_id=user_id)

            return GetTicketAmountRes(
                plinko=ticket.plinko_ticket_amount,
                yavarwee=ticket.yavarwee_ticket_amount,
                coinToss=ticket.coin_toss_ticket_amount
            )

    async def addition_ticket(self, data: TicketShopBuyReq):
        try:
            async with self.session.begin():
                ticket = await self.ticket_repository.find_ticket_amount_by_stage_id_and_user_id(stage_id=data.stageId, user_id=data.studentId)
                if ticket is None:
                    minigame = await self.minigame_repository.find_by_stage_id(data.stageId)
                    await self.ticket_repository.save(
                        Ticket(
                            minigame_id=minigame.minigame_id,
                            user_id=data.studentId,
                            coin_toss_ticket_amount=minigame.coin_toss_default_ticket_amount,
                            yavarwee_ticket_amount=minigame.yavarwee_default_ticket_amount,
                            plinko_ticket_amount=minigame.plinko_default_ticket_amount
                        )
                    )
                    await self.session.flush()
                    ticket = await self.ticket_repository.find_ticket_amount_by_stage_id_and_user_id(stage_id=data.stageId, user_id=data.studentId)

                if data.ticketType == TicketType.PLINKO:
                    ticket.plinko_ticket_amount += data.purchaseQuantity
                elif data.ticketType == TicketType.YAVARWEE:
                    ticket.yavarwee_ticket_amount += data.purchaseQuantity
                elif data.ticketType == TicketType.COINTOSS:
                    ticket.coin_toss_ticket_amount += data.purchaseQuantity

        except Exception:
             await EventProducer.create_event(
                topic='ticket_addition_failed',
                key=data.id,
                value=TicketEventFail(
                    id=data.id,
                    stageId=data.stageId,
                    studentId=data.studentId,
                    shopMiniGameId=data.shopMiniGameId,
                    ticketType=data.ticketType,
                    shopReceiptId=data.shopReceiptId,
                    ticketPrice=data.ticketPrice,
                    purchaseQuantity=data.purchaseQuantity
                ),
            )

             raise