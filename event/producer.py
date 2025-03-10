import logging

from kafka import KafkaProducer
import json

from pydantic import BaseModel

from config import KAFKA_HOST, KAFKA_PORT


producer = KafkaProducer(bootstrap_servers=f'{KAFKA_HOST}:{KAFKA_PORT}')


class EventProducer:
    @staticmethod
    async def create_event(topic, msg: BaseModel):
        try:
            producer.send(topic, json.dumps(msg.dict()).encode('utf-8'))
        except Exception as e:
            logging.error(e)