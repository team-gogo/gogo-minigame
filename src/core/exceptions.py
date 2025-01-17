from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException


class CustomException(APIException):
    status_code = 400
    default_code = 'default_code'
    default_detail = 'default_detail'


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code

    return response