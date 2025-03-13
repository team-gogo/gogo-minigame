from pydantic import BaseModel


class CreateStageShopGameDetails(BaseModel):
    isActive: int
    price: int | None = None
    quantity: int | None = None


class CreateStageShop(BaseModel):
    coinToss: CreateStageShopGameDetails
    yavarwee: CreateStageShopGameDetails
    plinko: CreateStageShopGameDetails


class CreateOfficialStageGameDetails(BaseModel):
    isActive: bool
    maxBettingPoint: int | None = None
    minBettingPoint: int | None = None


class CreateOfficialStageGameType(BaseModel):
    coinToss: CreateOfficialStageGameDetails
    yavarwee: CreateOfficialStageGameDetails
    plinko: CreateOfficialStageGameDetails


class CreateStageOfficial(BaseModel):
    id: str
    stageId: int
    miniGame: CreateOfficialStageGameType
    shop: CreateStageShop