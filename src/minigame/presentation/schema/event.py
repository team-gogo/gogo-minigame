from enum import Enum

from pydantic import BaseModel


class GameType(Enum):
    YAVARWEE = 'YAVARWEE'
    PLINKO = 'PLINKO'
    COINTOSS = 'COINTOSS'


class MinigameBetCompleted(BaseModel):
    id: str
    earnedPoint: int
    lostedPoint: int
    studentId: int
    stageId: int
    gameType: str