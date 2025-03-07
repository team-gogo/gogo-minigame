from abc import ABC, abstractmethod


class MinigameBetService(ABC):
    @abstractmethod
    async def bet(self, stage_id, user_id, data):
        pass