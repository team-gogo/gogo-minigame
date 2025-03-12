from pydantic import BaseModel


class IsCoinTossActive(BaseModel):
    isCoinTossActive :bool


class CreateStageFast(BaseModel):
    id: str
    stageId: int
    miniGame: IsCoinTossActive