from pydantic import BaseModel


class MinigameAdditionPoint(BaseModel):
    id: str
    point: int
    user_id: int