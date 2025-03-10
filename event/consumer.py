import json

from aiokafka import AIOKafkaConsumer
from kafka import KafkaConsumer

from config import KAFKA_HOST, KAFKA_PORT
from db import get_session
from event.schema.fast import CreateStageFast
from event.schema.official import CreateStageOfficial
from src.minigame.presentation.schema.minigame import MinigameCreateReq
from src.minigame.service.minigame import MinigameService




async def consume():
    consumer = AIOKafkaConsumer(
        'create_stage_fast', 'create_stage_official',
        bootstrap_servers=f'{KAFKA_HOST}:{KAFKA_PORT}'
    )

    await consumer.start()

    try:
        async for msg in consumer:
            if msg.topic == 'create_stage_fast':
                await EventController.create_stage_fast(msg)
            elif msg.topic == 'create_stage_official':
                await EventController.create_stage_official(msg)
    finally:
        await consumer.stop()


class EventController:
    @staticmethod
    async def create_stage_fast(msg):
        data = CreateStageFast(
            **json.loads(msg.value.decode('utf-8'))
        )
        session = await get_session()
        await MinigameService(session).create_minigame(
            MinigameCreateReq(
                stage_id=data.stageId,
                is_active_plinko=data.miniGame.isPlinkoActive,
                is_active_yavarwee=data.miniGame.isYavarweeActive,
                is_active_coin_toss=data.miniGame.isCoinTossActive
            )
        )

    @staticmethod
    async def create_stage_official(msg):
        data = CreateStageOfficial(
            **json.loads(msg.value.decode('utf-8'))
        )
        session = await get_session()
        await MinigameService(session).create_minigame(
            MinigameCreateReq(
                stage_id=data.stageId,
                is_active_plinko=data.is_active_plinko,
                is_active_yavarwee=data.is_active_yavarwee,
                is_active_coin_toss=data.is_active_coin_toss
            )
        )