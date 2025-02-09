from typing import Optional

from sqlmodel import Field, SQLModel


class Minigame(SQLModel, table=True):
    minigame_play_id: Optional[int] = Field(default=None, primary_key=True)
    minigame_id: int = Field(foreign_key='tbl_minigame.minigame_id', ondelete='CASCADE')
    student_id: int
    timestemp: str

    __tablename__ = 'tbl_minigame_play'
