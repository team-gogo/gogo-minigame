from typing import Annotated

from fastapi import APIRouter, Header, status, Depends
from starlette.websockets import WebSocket, WebSocketDisconnect
from websockets import ConnectionClosed

from src.minigame.factory import MinigameBetServiceFactory, Minigame
from src.yavarwee.presentation.schema.yavarwee import YavarweeBetReq
from authortiy import authority_student

router = APIRouter(prefix='/minigame/yavarwee')


@router.post('/{stage_id}')
async def coin_toss(
        stage_id: int,
        body: YavarweeBetReq,
        request_user_id: Annotated[int, Header()],
        authority: Annotated[str, Depends(authority_student)]
):
    service = await MinigameBetServiceFactory.create(Minigame.YAVARWEE)
    return await service.bet(stage_id=stage_id, user_id=request_user_id, data=body)