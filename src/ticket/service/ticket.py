from sqlmodel.ext.asyncio.session import AsyncSession

from event.schema.ticket import TicketType
from src.minigame.domain.model.minigame import Minigame
from src.minigame.domain.repository.minigame import MinigameRepository
from src.ticket.domain.repository.ticket import TicketRepository
from src.ticket.presentation.schema.ticket import GetTicketAmountRes
from src.ticket.domain.model.ticket import Ticket


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
                        user_id=user_id
                    )
                )
                await self.session.flush()
                ticket = await self.ticket_repository.find_ticket_amount_by_stage_id_and_user_id(stage_id=stage_id, user_id=user_id)

            await self.session.commit()

            return GetTicketAmountRes(
                plinko=ticket.plinko_ticket_amount,
                yavarwee=ticket.yavarwee_ticket_amount,
                coinToss=ticket.coin_toss_ticket_amount
            )

    async def addition_ticket(self, stage_id, user_id, ticket_amount, game):
        async with self.session.begin():
            ticket = await self.ticket_repository.find_ticket_amount_by_stage_id_and_user_id(stage_id=stage_id, user_id=user_id)
            if ticket is None:
                minigame = await self.minigame_repository.find_by_stage_id(stage_id)
                await self.ticket_repository.save(
                    Ticket(
                        minigame_id=minigame.minigame_id,
                        user_id=user_id
                    )
                )
                await self.session.flush()
                ticket = await self.ticket_repository.find_ticket_amount_by_stage_id_and_user_id(stage_id=stage_id, user_id=user_id)

            if game == TicketType.PLINKO:
                ticket.plinko_ticket_amount += ticket_amount
            elif game == TicketType.YAVARWEE:
                ticket.yavarwee_ticket_amount += ticket_amount
            elif game == TicketType.COINTOSS:
                ticket.coin_toss_ticket_amount += ticket_amount

            await self.session.commit()
