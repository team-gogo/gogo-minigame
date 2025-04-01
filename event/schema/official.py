from typing import Optional

from pydantic import BaseModel


class CreateStageShopGameDetails(BaseModel):
    isActive: int
    price: Optional[int] = None
    quantity: Optional[int] = None


class CreateStageShop(BaseModel):
    coinToss: CreateStageShopGameDetails
    yavarwee: CreateStageShopGameDetails
    plinko: CreateStageShopGameDetails


class CreateOfficialStageGameDetails(BaseModel):
    isActive: bool
    maxBettingPoint: Optional[int] = None
    minBettingPoint: Optional[int] = None
    initialTicketCount: Optional[int] = None


class CreateOfficialStageGameType(BaseModel):
    coinToss: CreateOfficialStageGameDetails
    yavarwee: CreateOfficialStageGameDetails
    plinko: CreateOfficialStageGameDetails


class CreateStageOfficial(BaseModel):
    id: str
    stageId: int
    miniGame: CreateOfficialStageGameType
    shop: CreateStageShop