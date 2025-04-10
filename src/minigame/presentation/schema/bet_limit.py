from typing import Optional

from pydantic import BaseModel


class MinigameBetLimitDetail(BaseModel):
    minBetPoint: Optional[int] = None
    maxBetPoint: Optional[int] = None


class MinigameBetLimitRes(BaseModel):
    plinko: MinigameBetLimitDetail
    yavarwee: MinigameBetLimitDetail
    coinToss: MinigameBetLimitDetail
