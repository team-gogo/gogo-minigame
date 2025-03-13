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
    shopId: int
    shopMiniGameId: int
    ticketType: TicketType
    shopReceiptId: int
    ticketPrice: int
    purchaseQuantity: int