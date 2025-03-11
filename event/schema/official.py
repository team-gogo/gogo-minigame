from pydantic import BaseModel

from event.schema.stage import CreateStageMinigameActive


class CreateStageShopGameDetails(BaseModel):
    isActive: int
    price: int | None = None
    quantity: int | None = None


class CreateStageShop(BaseModel):
    coinToss: CreateStageShopGameDetails
    yavarwee: CreateStageShopGameDetails
    plinko: CreateStageShopGameDetails


class CreateStageOfficial(BaseModel):
    id: str
    stageId: int
    miniGame: CreateStageMinigameActive
    shop: CreateStageShop