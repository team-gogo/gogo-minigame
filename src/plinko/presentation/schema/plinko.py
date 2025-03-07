from typing import List

from pydantic import BaseModel


class PlinkoBetRes(BaseModel):
    amount: float
    path: List[str]