from pydantic import BaseModel

from event.schema.stage import CreateStageMinigameActive


class CreateStageFast(BaseModel):
    id: str
    stageId: int
    miniGame: CreateStageMinigameActive