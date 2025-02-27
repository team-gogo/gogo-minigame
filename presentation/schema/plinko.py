from typing import List

from pydantic import BaseModel


class PlinkoBetRes(BaseModel):
    amount: int
    path: List[str]