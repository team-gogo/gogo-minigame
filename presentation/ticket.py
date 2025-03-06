from typing import Annotated

from fastapi import APIRouter, Header, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from db import get_session
from service.ticket import TicketService

router = APIRouter()


@router.get('/minigame/ticket/{stage_id}')
async def get_minigame_ticket(
        stage_id: int,
        request_user_id: Annotated[int, Header()],
        authority: Annotated[str, Header()],
        session: Annotated[AsyncSession, Depends(get_session)]
):
    if authority != 'STUDENT':
        raise HTTPException(status_code=403)

    return await TicketService(session).get_ticket_amount(request_user_id, stage_id)