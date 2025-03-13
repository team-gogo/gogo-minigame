from pydantic import BaseModel


class IsCoinTossActive(BaseModel):
    isCoinTossActive: bool
    coinTossMaxBettingPoint: int | None = None
    coinTossMinBettingPoint: int | None = None


class CreateStageFast(BaseModel):
    id: str
    stageId: int
    miniGame: IsCoinTossActive