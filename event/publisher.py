from event.producer import EventProducer
from src.minigame.presentation.schema.event import MinigameBetCompleted


class EventPublisher:

    @staticmethod
    async def minigame_bet_completed(uuid_, earned_point, losted_point, is_win, student_id, stage_id, game_type):
        await EventProducer.create_event(
            topic='minigame_bet_completed',
            key=uuid_,
            value=MinigameBetCompleted(
                id=uuid_,
                earnedPoint=earned_point,
                lostedPoint=losted_point,
                isWin=is_win,
                studentId=student_id,
                stageId=stage_id,
                gameType=game_type
            )
        )