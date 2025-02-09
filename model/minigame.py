from sqlmodel import Field, SQLModel


class Minigame(SQLModel, table=True):
    minigame_id: int = Field(default=None, primary_key=True)
    stage_id: int
    name: str
    is_active_coin_toss: bool
    is_active_plinko: bool
    is_active_yavarwee: bool

    __tablename__ = 'tbl_minigame'
