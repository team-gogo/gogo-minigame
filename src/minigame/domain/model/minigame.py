from enum import Enum
from typing import Optional

from sqlalchemy import Column, BigInteger
from sqlmodel import Field, SQLModel


class MinigameStatus(Enum):
    ABLE = "ABLE"
    PENDING = "PENDING"


class MinigameBetStatus(Enum):
    ROLLBACK = "ROLLBACK"
    CONFIRMED = "CONFIRMED"


class Minigame(SQLModel, table=True):
    minigame_id: int = Field(default=None, primary_key=True)
    stage_id: int = Field(sa_column=Column(BigInteger(), unique=True))

    is_active_coin_toss: bool = Field(default=False)
    is_active_plinko: Optional[bool] = Field(default=False)
    is_active_yavarwee: Optional[bool] = Field(default=False)

    coin_toss_default_ticket_amount: int = Field(nullable=True)
    yavarwee_default_ticket_amount: int = Field(nullable=True)
    plinko_default_ticket_amount: int = Field(nullable=True)

    status: MinigameStatus = Field(default=MinigameStatus.PENDING)

    coin_toss_max_betting_point: Optional[int] = Field(nullable=True)
    coin_toss_min_betting_point: Optional[int] = Field(nullable=True)
    coin_toss_initial_ticket_count: Optional[int] = Field(nullable=True)

    yavarwee_max_betting_point: Optional[int] = Field(nullable=True)
    yavarwee_min_betting_point: Optional[int] = Field(nullable=True)
    yavarwee_initial_ticket_count: Optional[int] = Field(nullable=True)

    plinko_max_betting_point: Optional[int] = Field(nullable=True)
    plinko_min_betting_point: Optional[int] = Field(nullable=True)
    plinko_initial_ticket_count: Optional[int] = Field(nullable=True)

    __tablename__ = 'tbl_minigame'
