import json

from aiokafka import AIOKafkaConsumer

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
                await EventConsumeService.create_stage(
                    CreateStageFast(**json.loads(msg.value.decode('utf-8')))
                )
            elif msg.topic == 'create_stage_official':
                await EventConsumeService.create_stage(
                    CreateStageOfficial(**json.loads(msg.value.decode('utf-8')))
                )
    finally:
        await consumer.stop()


class EventConsumeService:
    @staticmethod
    async def create_stage(data):
        session = await get_session()
        await MinigameService(session).create_minigame(
            MinigameCreateReq(
                stage_id=data.stageId,
                is_active_plinko=data.miniGame.isPlinkoActive,
                is_active_yavarwee=data.miniGame.isYavarweeActive,
                is_active_coin_toss=data.miniGame.isCoinTossActive
            )
        )
