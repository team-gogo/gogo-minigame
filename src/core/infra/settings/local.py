from .base import *


ALLOWED_HOSTS = ['*']

eureka_client.init(
    eureka_server='http://127.0.0.1:8761',
    app_name='gogo-minigame',
    instance_port=8086
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gogo-minigame',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}