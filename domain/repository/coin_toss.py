from sqlmodel.ext.asyncio.session import AsyncSession

from domain.model.coin_toss import CoinTossResult


class CoinTossRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, coin_toss_result: CoinTossResult):
        self.session.add(coin_toss_result)