import json
import logging

from aiokafka import AIOKafkaConsumer

from config import KAFKA_HOST, KAFKA_PORT
from event.controller import EventConsumeController
from event.schema.fast import CreateStageFast
from event.schema.official import CreateStageOfficial
from event.schema.stage import StageConfirmReq
from event.schema.ticket import TicketShopBuyReq


async def consume():
    consumer = AIOKafkaConsumer(
        'stage_create_fast', 'stage_create_official', 'stage_confirm',
        'ticket_point_minus',
        bootstrap_servers=f'{KAFKA_HOST}:{KAFKA_PORT}'
    )

    await consumer.start()
    try:
        async for msg in consumer:
            data = json.loads(msg.value.decode('utf-8'))
            logging.info(f'Consume kafka data {data.topic} value: {data}')
            if msg.topic == 'stage_create_fast':
                await EventConsumeController.create_stage_fast(CreateStageFast(**data))
            elif msg.topic == 'stage_create_official':
                await EventConsumeController.create_stage_official(CreateStageOfficial(**data))
            elif msg.topic == 'stage_confirm':
                await EventConsumeController.stage_confirm(StageConfirmReq(**data))
            elif msg.topic == 'ticket_point_minus':
                await EventConsumeController.ticket_buy(TicketShopBuyReq(**data))
    except Exception as e:
        logging.exception(f'Kafka consume exception {str(e)}')
    finally:
        await consumer.stop()
