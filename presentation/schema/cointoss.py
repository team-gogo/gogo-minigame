from pydantic import BaseModel


class CoinTossBetRes(BaseModel):
    result: bool
    amount: int