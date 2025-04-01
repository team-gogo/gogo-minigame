from pydantic import BaseModel


class CreateStageMinigameActive(BaseModel):
    isCoinTossActive: bool
    isYavarweeActive: bool
    isPlinkoActive: bool


class StageConfirmReq(BaseModel):
    id: str
    stageId: int