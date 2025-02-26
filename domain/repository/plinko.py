from sqlmodel.ext.asyncio.session import AsyncSession

from domain.model.plinko_result import PlinkoResult


class PlinkoRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, plinko_result: PlinkoResult):
        self.session.add(plinko_result)