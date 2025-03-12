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
        'ticket_shop_buy', 'ticket_buy_point_minus',
        bootstrap_servers=f'{KAFKA_HOST}:{KAFKA_PORT}'
    )

    await consumer.start()

    try:
        async for msg in consumer:
            try:
                data = json.loads(msg.value.decode('utf-8'))
                if msg.topic == 'stage_create_fast':
                    await EventConsumeController.create_stage_fast(CreateStageFast(**data))
                elif msg.topic == 'stage_create_official':
                    await EventConsumeController.create_stage_official(CreateStageOfficial(**data))
                elif msg.topic == 'stage_confirm':
                    await EventConsumeController.stage_confirm(StageConfirmReq(**data))
                elif msg.topic == 'ticket_shop_buy':
                    await EventConsumeController.ticket_buy(TicketShopBuyReq(**data))
            except Exception as e:
                logging.error(f'kafka consume format error = ' + str(e))

    finally:
        await consumer.stop()


