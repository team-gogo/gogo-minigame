from sqlmodel.ext.asyncio.session import AsyncSession

from domain.model.play import Play


class PlayRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, play: Play):
        self.session.add(play)