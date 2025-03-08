from pydantic import BaseModel
from pydantic import UUID4


class YavarweeBetReq(BaseModel):
    proof: str
    uuid: UUID4
    amount: int
    round: int


class YavarweeBetRes(BaseModel):
    amount: int