from sqlmodel.ext.asyncio.session import AsyncSession

from src.plinko.domain.model.plinko_result import PlinkoResult


class PlinkoResultRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, plinko_result: PlinkoResult):
        self.session.add(plinko_result)