from pydantic import BaseModel
from pydantic import UUID4


class YavarweeBetDetail(BaseModel):
    uuid: UUID4
    amount: int
    round: int


class YavarweeBetReq(BaseModel):
    data: str


class YavarweeBetRes(BaseModel):
    amount: int