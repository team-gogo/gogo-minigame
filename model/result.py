from typing import Optional

from sqlmodel import Field, SQLModel, Column, Enum



class Result(SQLModel, table=True):
    minigame_result_id: Optional[int] = Field(default=None, primary_key=True)
    minigame_bet_id: int = Field(foreign_key='tbl_minigame_bet.minigame_bet_id', ondelete='CASCADE')
    point: int

    __tablename__ = 'tbl_minigame_result'
