from typing import Optional

from sqlmodel import SQLModel, Field


class Ticket(SQLModel, table=True):
    ticket_id: Optional[int] = Field(default=None, primary_key=True)
    minigame_id: Optional[int] = Field(foreign_key='tbl_minigame.minigame_id', ondelete='CASCADE')
    user_id: int
    coin_toss_ticket_amount: int
    plinko_ticket_amount: int
    yavarwee_ticket_amount: int

    __tablename__ = 'tbl_minigame_ticket'
