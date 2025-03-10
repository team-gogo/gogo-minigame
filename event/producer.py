from aiokafka import AIOKafkaProducer
import json

from pydantic import BaseModel

from config import KAFKA_HOST, KAFKA_PORT


class EventProducer:
    @staticmethod
    async def create_event(topic, msg: BaseModel):
        producer = AIOKafkaProducer(bootstrap_servers=f'{KAFKA_HOST}:{KAFKA_PORT}')
        await producer.start()
        await producer.send_and_wait(topic, json.dumps(msg.dict()).encode('utf-8'))
        await producer.stop()