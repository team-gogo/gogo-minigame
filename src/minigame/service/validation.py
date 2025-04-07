import json

from py_eureka_client.eureka_client import do_service_async
from fastapi import status, HTTPException

from src.minigame.domain.model.minigame import MinigameStatus, Minigame


class BetValidationService:
    @staticmethod
    async def validate_minigame_status(minigame: Minigame):
        if minigame.status == MinigameStatus.PENDING:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Stage is not available')

    @staticmethod
    async def is_student_participate_in_stage(stage_id, student_id):
        validate_stage_student_response = await do_service_async('gogo-stage', f'/stage/api/participant/{stage_id}?studentId={student_id}')
        if not validate_stage_student_response:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='gogo-stage no response')
        if not json.loads(validate_stage_student_response)['isParticipant']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not a participant')