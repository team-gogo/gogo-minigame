from typing import Annotated

from fastapi import APIRouter, Depends, Header, Body

from authortiy import authority_student
from src.cointoss.presentation.schema.cointoss import CoinTossBetReq
from src.minigame.factory import MinigameBetServiceFactory, Minigame

router = APIRouter(prefix='/minigame/coin-toss')


@router.post('/{stage_id}')
async def coin_toss(
        stage_id: int,
        body: CoinTossBetReq,
        request_user_id: Annotated[int, Header()],
        authority: Annotated[str, Depends(authority_student)]
):
    service = await MinigameBetServiceFactory.create(Minigame.COIN_TOSS)
    return await service.bet(stage_id=stage_id, user_id=request_user_id, data=body)
