from enum import Enum

from fastapi import Header, HTTPException


class Role(Enum):
    USER = 'USER'
    STAFF = 'STAFF'
    DEVELOPER = 'DEVELOPER'


def authority_student(request_user_authority: str = Header(...)):
    if request_user_authority in (Role.USER.value, Role.STAFF.value):
        raise HTTPException(status_code=403, detail='Authority must be "USER"')
    return request_user_authority
