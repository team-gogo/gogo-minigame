from enum import Enum

from db import get_session
from src.minigame.service.impl.cointoss import CoinTossMinigameBetServiceImpl
from src.minigame.service.impl.plinko import PlinkoMinigameBetServiceImpl
from src.minigame.service.impl.yavarwee import YavarweeMinigameBetServiceImpl


class Minigame(Enum):
    COIN_TOSS = 'coin_toss'
    PLINKO = 'plinko'
    YAVARWEE = 'yavarwee'


class MinigameBetServiceFactory:
    @staticmethod
    async def create(game: Minigame):
        session = await get_session()

        if game == Minigame.COIN_TOSS:
            return CoinTossMinigameBetServiceImpl(session=session)
        elif game == Minigame.PLINKO:
            return PlinkoMinigameBetServiceImpl(session=session)
        elif game == Minigame.YAVARWEE:
            return YavarweeMinigameBetServiceImpl(session=session)