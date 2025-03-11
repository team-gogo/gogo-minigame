import base64
from hashlib import pbkdf2_hmac
from uuid import UUID

from fastapi import WebSocketException, status

from config import YAVARWEE_SECRET
from src.minigame.domain.model.minigame import MinigameStatus, Minigame


class BetValidationService:
    @staticmethod
    async def validate_proof(uuid: UUID, amount: int, round_: int) -> None:
        my_hash = pbkdf2_hmac(
            'sha256',
            f'{uuid}{amount}{round_}'.encode('utf-8'),
            str(YAVARWEE_SECRET).encode('utf-8'),
            100000
        )

        d_proof = base64.b64encode(my_hash).decode('utf-8')
        proof = base64.b64decode(d_proof)

        if not my_hash == proof:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason='Proof fail.')

    @staticmethod
    async def validate_minigame_status(minigame: Minigame):
        if minigame.status == MinigameStatus.PENDING:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason='Stage is not available')
