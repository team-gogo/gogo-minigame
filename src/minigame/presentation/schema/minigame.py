from pydantic import BaseModel


class GetActiveMinigameRes(BaseModel):
    isPlinkoActive: bool
    isCoinTossActive: bool
    isYavarweeActive: bool


class MinigameCreateReq(BaseModel):
    stage_id: int
    is_active_coin_toss: bool
    is_active_plinko: bool | None = None
    is_active_yavarwee: bool | None = None

    coin_toss_max_betting_point: int | None = None
    coin_toss_min_betting_point: int | None = None

    yavarwee_max_betting_point: int | None = None
    yavarwee_min_betting_point: int | None = None

    plinko_max_betting_point: int | None = None
    plinko_min_betting_point: int | None = None