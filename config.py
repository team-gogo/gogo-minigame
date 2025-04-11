import os

from dotenv import load_dotenv


load_dotenv('.env')


DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

EUREKA_HOST = os.environ.get('EUREKA_HOST')
EUREKA_PORT = os.environ.get('EUREKA_PORT')
EUREKA_SERVICE_NAME = os.environ.get('EUREKA_SERVICE_NAME')
INSTANCE_IP = os.environ.get('INSTANCE_IP')
INSTANCE_HOST = os.environ.get('INSTANCE_HOST')
INSTANCE_PORT = int(os.environ.get('INSTANCE_PORT'))

KAFKA_HOST = os.environ.get('KAFKA_HOST')
KAFKA_PORT = os.environ.get('KAFKA_PORT')

YAVARWEE_PRIVATE_KEY = os.environ.get('YAVARWEE_PRIVATE_KEY')

LOKI_ENDPOINT = os.environ.get('LOKI_ENDPOINT')