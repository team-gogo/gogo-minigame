from py_eureka_client import eureka_client

from config import EUREKA_HOST, EUREKA_PORT, EUREKA_SERVICE_NAME, INSTANCE_PORT


EUREKA_SERVER = f'http://{EUREKA_HOST}:{EUREKA_PORT}'

def init_eureka():
    eureka_client.init_async(
        eureka_server = EUREKA_SERVER,
        app_name=EUREKA_SERVICE_NAME,
        instance_port=INSTANCE_PORT
    )