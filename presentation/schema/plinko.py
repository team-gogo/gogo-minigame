from typing import List

from pydantic import BaseModel


class PlinkoBetRes(BaseModel):
    amount: str
    path: List[str]