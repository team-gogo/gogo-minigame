from pydantic import BaseModel


class CoinTossBetReq(BaseModel):
    amount: int


class CoinTossBetRes(BaseModel):
    result: bool
    amount: int