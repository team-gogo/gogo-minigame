from pydantic import BaseModel


class CoinTossBetType(BaseModel):
    FRONT = 'FRONT'
    BACK = 'BACK'


class CoinTossBetReq(BaseModel):
    amount: int
    bet: CoinTossBetType


class CoinTossBetRes(BaseModel):
    result: bool
    amount: int