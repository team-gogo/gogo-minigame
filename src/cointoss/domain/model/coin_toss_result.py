from typing import Optional

from sqlmodel import SQLModel, Field


class CoinTossResult(SQLModel, table=True):
    coin_toss_result_id: Optional[int] = Field(default=None, primary_key=True)
    minigame_id: int = Field(foreign_key='tbl_minigame.minigame_id', ondelete='CASCADE')
    student_id: int
    timestamp: int
    bet_point: int
    result: bool
    point: int

    __tablename__ = 'tbl_coin_toss_result'