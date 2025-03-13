from typing import Optional

from pydantic import BaseModel


class GetActiveMinigameRes(BaseModel):
    isPlinkoActive: bool
    isCoinTossActive: bool
    isYavarweeActive: bool


class MinigameCreateReq(BaseModel):
    stage_id: int
    is_active_coin_toss: bool
    is_active_plinko: Optional[bool] = None
    is_active_yavarwee: Optional[bool] = None

    coin_toss_max_betting_point: Optional[int] = None
    coin_toss_min_betting_point: Optional[int] = None

    yavarwee_max_betting_point: Optional[int] = None
    yavarwee_min_betting_point: Optional[int] = None

    plinko_max_betting_point: Optional[int] = None
    plinko_min_betting_point: Optional[int] = None