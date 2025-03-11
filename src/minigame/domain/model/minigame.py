from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class MinigameStatus(Enum):
    ACTIVE = "ACTIVE"
    PENDING = "PENDING"


class Minigame(SQLModel, table=True):
    minigame_id: int = Field(default=None, primary_key=True)
    stage_id: int = Field(unique=True)
    is_active_coin_toss: bool = Field(default=False)
    is_active_plinko: Optional[bool] = Field(default=False)
    is_active_yavarwee: Optional[bool] = Field(default=False)
    status: MinigameStatus = Field(default=MinigameStatus.PENDING)

    __tablename__ = 'tbl_minigame'
