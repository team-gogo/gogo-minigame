from fastapi import Header


def authority_student(authority: str = Header(...)):
    if authority != 'STUDENT':
        raise Exception('Authority must be "STUDENT"')
    return authority
