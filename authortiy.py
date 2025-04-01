from enum import Enum

from fastapi import Header, HTTPException, status


class Role(Enum):
    USER = 'USER'
    STAFF = 'STAFF'
    DEVELOPER = 'DEVELOPER'


def authority_student(request_user_authority: str = Header(...)):
    if request_user_authority not in (Role.USER.value, Role.STAFF.value):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authority must be USER')
    return request_user_authority
