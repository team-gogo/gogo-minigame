import base64
import json
from hashlib import pbkdf2_hmac
from uuid import UUID

from py_eureka_client.eureka_client import do_service_async
from fastapi import status, HTTPException

from config import YAVARWEE_SECRET
from src.minigame.domain.model.minigame import MinigameStatus, Minigame


class BetValidationService:
    # Todo: sha logic
    @staticmethod
    async def validate_proof(uuid: UUID, amount: int, round_: int, proof: str) -> None:
        my_hash = pbkdf2_hmac(
            'sha256',
            f'{uuid}{amount}{round_}'.encode('utf-8'),
            str(YAVARWEE_SECRET).encode('utf-8'),
            100000
        )

        user_proof = base64.b64decode(proof)

        if not my_hash == user_proof:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Proof fail.')

    @staticmethod
    async def validate_minigame_status(minigame: Minigame):
        if minigame.status == MinigameStatus.PENDING:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Stage is not available')

    @staticmethod
    async def validate_plinko_status(stage_id, student_id):
        validate_stage_student_response = await do_service_async('gogo-stage', f'/api/participant/{stage_id}?studentId={student_id}')
        if not validate_stage_student_response:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='gogo-stage no response')
        if not json.loads(validate_stage_student_response)['isParticipant']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not a participant')