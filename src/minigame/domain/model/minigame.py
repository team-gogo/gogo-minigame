from enum import Enum
from typing import Optional

from sqlalchemy import Column, BigInteger
from sqlmodel import Field, SQLModel


class MinigameStatus(Enum):
    ACTIVE = "ACTIVE"
    PENDING = "PENDING"


class Minigame(SQLModel, table=True):
    minigame_id: int = Field(default=None, primary_key=True)
    stage_id: int = Field(sa_column=Column(BigInteger(), unique=True))
    is_active_coin_toss: bool = Field(default=False)
    is_active_plinko: Optional[bool] = Field(default=False)
    is_active_yavarwee: Optional[bool] = Field(default=False)
    status: MinigameStatus = Field(default=MinigameStatus.PENDING)

    coin_toss_max_betting_point: Optional[int] = Field(default=None)
    coin_toss_min_betting_point: Optional[int] = Field(default=None)

    yavarwee_max_betting_point: Optional[int] = Field(default=None)
    yavarwee_min_betting_point: Optional[int] = Field(default=None)

    plinko_max_betting_point: Optional[int] = Field(default=None)
    plinko_min_betting_point: Optional[int] = Field(default=None)

    __tablename__ = 'tbl_minigame'
