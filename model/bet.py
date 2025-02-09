from typing import Optional

from sqlmodel import Field, SQLModel, Column, Enum


class CoinTossType(str, Enum):
    FRONT = 'FRONT'
    BACK = 'BACK'


class Bet(SQLModel, table=True):
    minigame_bet_id: Optional[int] = Field(default=None, primary_key=True)
    minigame_play_id: int = Field(foreign_key='tbl_minigame_play.minigame_play_id', ondelete='CASCADE')
    bet_point: int
    coin_toss: Optional[CoinTossType]
    yavarwee_stage: Optional[int]
    plinko_point: Optional[int]

    __tablename__ = 'tbl_minigame_bet'

    class Config:
        arbitrary_types_allowed = True