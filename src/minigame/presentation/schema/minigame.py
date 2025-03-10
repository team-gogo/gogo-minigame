from pydantic import BaseModel


class GetActiveMinigameRes(BaseModel):
    isPlinkoActive: bool
    isCoinTossActive: bool
    isYavarweeActive: bool


class MinigameCreateReq(BaseModel):
    stage_id: int
    is_active_coin_toss: bool
    is_active_plinko: bool
    is_active_yavarwee: bool