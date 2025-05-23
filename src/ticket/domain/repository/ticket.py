from typing import Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.minigame.domain.repository.minigame import Minigame
from src.ticket.domain.model.ticket import Ticket


class TicketRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_minigame_id_and_user_id_for_update(self, minigame_id, user_id) -> Optional[Ticket]:
        statement = select(Ticket).where(Ticket.minigame_id == minigame_id, Ticket.user_id == user_id).with_for_update()
        result = await self.session.exec(statement)
        return result.first()

    async def find_ticket_amount_by_stage_id_and_student_id(self, stage_id, student_id) -> Optional[Ticket]:
        statement = (
            select(Ticket)
            .join(Minigame)
            .where(Minigame.stage_id == stage_id, Ticket.student_id == student_id)
            .with_for_update()
        )
        result = await self.session.exec(statement)
        return result.first()

    async def save(self, data):
        self.session.add(data)