from typing import Annotated

from fastapi import APIRouter, Header, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from authortiy import authority_student
from db import get_session
from src.ticket.service.ticket import TicketService

router = APIRouter()


@router.get('/minigame/ticket/{stage_id}')
async def get_minigame_ticket(
        stage_id: int,
        request_user_id: Annotated[int, Header()],
        authority: Annotated[str, Depends(authority_student)],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    return await TicketService(session).get_ticket_amount(request_user_id, stage_id)