import os

from dotenv import load_dotenv


load_dotenv('.env')


def _required_env(name: str) -> str:
    value = os.environ.get(name)
    if value is None or not value.strip():
        raise ValueError(f'{name} is required')
    return value


DB_HOST = _required_env('DB_HOST')
_db_port = _required_env('DB_PORT')
try:
    DB_PORT = int(_db_port)
except ValueError:
    raise ValueError('DB_PORT must be an integer') from None
DB_NAME = _required_env('DB_NAME')
DB_USER = _required_env('DB_USER')
DB_PASS = _required_env('DB_PASS')

KAFKA_HOST = os.environ.get('KAFKA_HOST')
KAFKA_PORT = os.environ.get('KAFKA_PORT')

YAVARWEE_PRIVATE_KEY = os.environ.get('YAVARWEE_PRIVATE_KEY')

LOKI_ENDPOINT = os.environ.get('LOKI_ENDPOINT')