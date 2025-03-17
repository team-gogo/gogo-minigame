from typing import Optional

from sqlalchemy import Column, BigInteger
from sqlmodel import SQLModel, Field


class Ticket(SQLModel, table=True):
    ticket_id: Optional[int] = Field(default=None, primary_key=True)
    minigame_id: Optional[int] = Field(foreign_key='tbl_minigame.minigame_id', ondelete='CASCADE')
    user_id: int = Field(sa_column=Column(BigInteger()))
    coin_toss_ticket_amount: int = Field(sa_column=Column(BigInteger(), default=0))
    plinko_ticket_amount: int = Field(sa_column=Column(BigInteger(), default=0))
    yavarwee_ticket_amount: int = Field(sa_column=Column(BigInteger(), default=0))

    __tablename__ = 'tbl_minigame_ticket'