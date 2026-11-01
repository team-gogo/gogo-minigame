import asyncio
import json
import logging
import os

from aiokafka import AIOKafkaConsumer

from config import KAFKA_HOST, KAFKA_PORT
from event.topic import event_topic


async def consume(ready: asyncio.Event):
    logger = logging.getLogger('GOGO-MiniGame Logger')
    while True:
        consumer = AIOKafkaConsumer(
            'stage_create_fast', 'stage_create_official', 'stage_confirm',
            'ticket_point_minus',
            bootstrap_servers=f'{KAFKA_HOST}:{KAFKA_PORT}',
            group_id=os.environ.get('KAFKA_GROUP_ID', 'gogo-minigame'),
            auto_offset_reset='earliest',
            enable_auto_commit=False,
        )
        try:
            await consumer.start()
            ready.set()
            async for msg in consumer:
                data = json.loads(msg.value.decode('utf-8'))
                class_, schema_ = event_topic[msg.topic]
                await class_(schema_(**data))
                await consumer.commit()
        except Exception:
            logger.exception('Kafka consumer failed; reconnecting')
        finally:
            ready.clear()
            await consumer.stop()
        if not ready.is_set():
            await asyncio.sleep(5)