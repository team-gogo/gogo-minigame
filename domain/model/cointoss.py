from pydantic import BaseModel


class CoinTossBetRes(BaseModel):
    result: str
    amount: int