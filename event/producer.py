import json

from aiokafka import AIOKafkaProducer
from pydantic import BaseModel

from config import KAFKA_HOST, KAFKA_PORT


class EventProducer:
    @staticmethod
    async def create_event(topic: str, key: str, value: BaseModel):
        producer = AIOKafkaProducer(bootstrap_servers=f'{KAFKA_HOST}:{KAFKA_PORT}')
        await producer.start()
        await producer.send_and_wait(
            key=key,
            topic=topic,
            value=json.dumps(value.dict()).encode('utf-8'),
        )
        await producer.stop()
