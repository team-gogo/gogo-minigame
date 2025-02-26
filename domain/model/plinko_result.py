from typing import Optional

from sqlmodel import SQLModel, Field


class PlinkoResult(SQLModel, table=True):
    plinko_result_id: Optional[int] = Field(default=None, primary_key=True)
    minigame_play_id: int = Field(foreign_key='tbl_minigame_play.minigame_play_id', ondelete='CASCADE')
    minigame_id: int = Field(foreign_key='tbl_minigame.minigame_id', ondelete='CASCADE')
    student_id: int = Field(foreign_key='tbl_student.student_id', ondelete='CASCADE')
    timestamp: str
    bet_point: int
    result: float
    point: int

    __tablename__ = 'tbl_plinko_result'