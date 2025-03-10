from uuid import UUID

from pydantic import BaseModel


class MinigameAdditionPoint(BaseModel):
    uuid: UUID | None = None
    point: int
    user_id: int