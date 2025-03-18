from enum import Enum
from typing import List

from pydantic import BaseModel


class PlinkoRiskType(Enum):
    HIGH = 'HIGH'
    MEDIUM = 'MEDIUM'
    LOW = 'LOW'


class PlinkoBetReq(BaseModel):
    amount: int
    risk: PlinkoRiskType


class PlinkoBetRes(BaseModel):
    amount: float
    path: List[str]
    multi: int