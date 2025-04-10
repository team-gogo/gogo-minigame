from enum import Enum
from pydantic import BaseModel


class CoinTossBetType(Enum):
    FRONT = 'FRONT'
    BACK = 'BACK'


class CoinTossBetReq(BaseModel):
    amount: int
    bet: CoinTossBetType


class CoinTossBetRes(BaseModel):
    result: bool
    amount: int
