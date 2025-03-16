from enum import Enum

from fastapi import Header
from starlette.exceptions import WebSocketException
from starlette.status import WS_1008_POLICY_VIOLATION


class Role(Enum):
    USER = 'USER'
    STAFF = 'STAFF'
    DEVELOPER = 'DEVELOPER'


def authority_student(request_user_authority: str = Header(...)):
    if request_user_authority not in (Role.USER.value, Role.STAFF.value):
        raise WebSocketException(code=WS_1008_POLICY_VIOLATION, reason='Authority must be "USER"')
    return request_user_authority
