from sqlmodel.ext.asyncio.session import AsyncSession

from src.cointoss.domain.model.coin_toss_result import CoinTossResult


class CoinTossResultRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, coin_toss_result: CoinTossResult):
        self.session.add(coin_toss_result)