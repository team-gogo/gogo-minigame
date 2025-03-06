from sqlmodel.ext.asyncio.session import AsyncSession

from domain.repository.ticket import TicketRepository
from presentation.schema.ticket import GetTicketAmountRes


class TicketService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.ticket_repository = TicketRepository(session)

    async def get_ticket_amount(self, user_id, stage_id):
        async with self.session.begin():
            ticket = await self.ticket_repository.find_ticket_amount_by_stage_id_and_user_id(user_id, stage_id)
            return GetTicketAmountRes(
                plinko=ticket.plinko_ticket_amount,
                yavarwee=ticket.yavarwee_ticket_amount,
                coinToss=ticket.coin_toss_ticket_amount
            )