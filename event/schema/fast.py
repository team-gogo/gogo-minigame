from typing import Optional

from pydantic import BaseModel


class CoinTossDetail(BaseModel):
    isCoinTossActive: bool
    coinTossMaxBettingPoint: Optional[int] = None
    coinTossMinBettingPoint: Optional[int] = None
    coinTossInitialTicketCount: Optional[int] = None


class CreateStageFast(BaseModel):
    id: str
    stageId: int
    miniGame: CoinTossDetail