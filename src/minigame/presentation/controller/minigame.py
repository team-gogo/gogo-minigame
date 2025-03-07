from typing import Annotated

from fastapi import APIRouter, Header, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from authortiy import authority_student
from db import get_session
from src.minigame.service.minigame import MinigameService

router = APIRouter()


@router.get('/minigame/active-game/{stage_id}')
async def minigame_active_game(
        stage_id: int,
        request_user_id: Annotated[int, Header()],
        authority: Annotated[str, Depends(authority_student)],
        session: Annotated[AsyncSession, Depends(get_session)]
):
    if authority != 'STUDENT':
        raise HTTPException(status_code=403)

    return await MinigameService(session).get_active_minigame(stage_id)