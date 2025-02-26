from typing import Optional

from sqlmodel import SQLModel, Field


class YavarweeResult(SQLModel, table=True):
    yavarwee_result_id: Optional[int] = Field(default=None, primary_key=True)
    minigame_play_id: int = Field(foreign_key='tbl_minigame_play.minigame_play_id', ondelete='CASCADE')
    minigame_id: int = Field(foreign_key='tbl_minigame.minigame_id', ondelete='CASCADE')
    student_id: int = Field(foreign_key='tbl_student.student_id', ondelete='CASCADE')
    timestamp: str
    yavarwee_stage: int  # 1~5
    point: int

    __tablename__ = 'tbl_yavarwee_result'