from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class MinigameAdditionPoint(BaseModel):
    uuid: Optional[UUID] = None

    point: int
    user_id: int