from pydantic import BaseModel
from pydantic import UUID4


class YavarweeBetReq(BaseModel):
    amount: int


class YavarweeBetRes(BaseModel):
    uuid: str


class YavarweeBetConfirmDetail(BaseModel):
    uuid: UUID4
    round: int
    status: bool


class YavarweeBetConfirmReq(BaseModel):
    data: str