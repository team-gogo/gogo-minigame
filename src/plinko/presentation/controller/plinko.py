from typing import Annotated

from fastapi import APIRouter, WebSocketDisconnect, WebSocket, status, Depends
from fastapi.params import Header
from websockets import ConnectionClosed

from authortiy import authority_student
from src.plinko.presentation.schema.plinko import PlinkoBetReq
from src.minigame.factory import MinigameBetServiceFactory, Minigame

router = APIRouter(prefix='/minigame/plinko')


@router.post('/{stage_id}')
async def coin_toss(
        stage_id: int,
        body: PlinkoBetReq,
        request_user_id: Annotated[int, Header()],
        authority: Annotated[str, Depends(authority_student)]
):
    service = await MinigameBetServiceFactory.create(Minigame.PLINKO)
    return await service.bet(stage_id=stage_id, user_id=request_user_id, data=body)
