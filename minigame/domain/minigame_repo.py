from sqlmodel import select

from .minigame import Minigame


async def find_minigame_by_stage_id(session, stage_id):
    minigame_select = select(Minigame).where(Minigame.stage_id == stage_id)
    minigame = await session.exec(minigame_select)
    return minigame.first()
