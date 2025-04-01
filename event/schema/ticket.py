from enum import Enum

from pydantic import BaseModel


class TicketType(Enum):
    YAVARWEE = 'YAVARWEE'
    PLINKO = 'PLINKO'
    COINTOSS = 'COINTOSS'


class TicketShopBuyReq(BaseModel):
    id: str
    stageId: int
    studentId: int
    shopMiniGameId: int
    ticketType: TicketType
    ticketPrice: int
    purchaseQuantity: int