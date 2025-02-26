from typing import Optional
from sqlmodel import SQLModel, Field


class CoinTossResult(SQLModel, table=True):
    coin_toss_result_id: Optional[int] = Field(default=None, primary_key=True)
    minigame_play_id: int = Field(foreign_key='tbl_minigame_play.minigame_play_id', ondelete='CASCADE')
    student_id: int = Field(foreign_key='tbl_student.student_id', ondelete='CASCADE')
    timestamp: str
    bet_point: int
    result: bool
    point: int

    __tablename__ = 'tbl_coin_toss_result'