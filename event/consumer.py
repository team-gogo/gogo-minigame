import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer

from config import KAFKA_HOST, KAFKA_PORT
from event.topic import event_topic


async def consume():
    while True:
        try:
            consumer = AIOKafkaConsumer(
                'stage_create_fast', 'stage_create_official', 'stage_confirm',
                'ticket_point_minus',
                bootstrap_servers=f'{KAFKA_HOST}:{KAFKA_PORT}'
            )

            await consumer.start()
            try:
                async for msg in consumer:
                    data = json.loads(msg.value.decode('utf-8'))
                    logging.info(f'Consume kafka data {msg.topic} value: {data}')

                    class_, schema_ = event_topic[msg.topic]
                    await class_(schema_(**data))
            except Exception as e:
                logging.exception(f'Kafka consume exception {str(e)}')

        except Exception as e:
            logging.exception(f'Kafka consumer is stop error {str(e)}')
            await asyncio.sleep(5)