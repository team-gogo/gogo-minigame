from datetime import datetime
from typing import Optional

from sqlalchemy import Column, BigInteger
from sqlmodel import SQLModel, Field

from src.minigame.domain.model.minigame import MinigameBetStatus


class PlinkoResult(SQLModel, table=True):
    plinko_result_id: Optional[int] = Field(default=None, primary_key=True)
    minigame_id: int = Field(foreign_key='tbl_minigame.minigame_id', ondelete='CASCADE')
    student_id: int = Field(sa_column=Column(BigInteger()))
    timestamp: datetime = Field(default=datetime.now())
    bet_point: int = Field(sa_column=Column(BigInteger()))
    result: float
    point: int = Field(sa_column=Column(BigInteger()))
    uuid: str = Field(unique=True)
    status: MinigameBetStatus

    __tablename__ = 'tbl_plinko_result'
