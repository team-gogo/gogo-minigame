from pydantic import BaseModel


class GetActiveMinigameRes(BaseModel):
    isPlinkoActive: bool
    isCoinTossActive: bool
    isYavarweeActive: bool