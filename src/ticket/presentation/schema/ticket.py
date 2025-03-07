from pydantic import BaseModel


class GetTicketAmountRes(BaseModel):
    plinko: int
    yavarwee: int
    coinToss: int