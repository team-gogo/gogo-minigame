import json

from aiokafka import AIOKafkaConsumer

from config import KAFKA_HOST, KAFKA_PORT
from db import get_session
from event.schema.fast import CreateStageFast
from event.schema.official import CreateStageOfficial
from event.schema.stage import StageConfirmReq
from src.minigame.presentation.schema.minigame import MinigameCreateReq
from src.minigame.service.minigame import MinigameService


async def consume():
    consumer = AIOKafkaConsumer(
        'stage_create_fast', 'stage_create_official', 'stage_confirm',
        bootstrap_servers=f'{KAFKA_HOST}:{KAFKA_PORT}'
    )

    await consumer.start()

    try:
        async for msg in consumer:
            data = json.loads(msg.value.decode('utf-8'))
            if msg.topic == 'stage_create_fast':
                await EventConsumeController.create_stage_fast(CreateStageFast(**data))
            elif msg.topic == 'stage_create_official':
                await EventConsumeController.create_stage_official(CreateStageOfficial(**data))
            elif msg.topic == 'stage_confirm':
                await EventConsumeController.stage_confirm(StageConfirmReq(**data))
    finally:
        await consumer.stop()


class EventConsumeController:
    @staticmethod
    async def create_stage_fast(data: CreateStageFast):
        session = await get_session()
        await MinigameService(session).create_minigame(
            MinigameCreateReq(
                stage_id=data.stageId,
                is_active_coin_toss=data.miniGame.isCoinTossActive
            )
        )

    @staticmethod
    async def create_stage_official(data):
        session = await get_session()
        await MinigameService(session).create_minigame(
            MinigameCreateReq(
                stage_id=data.stageId,
                is_active_plinko= data.miniGame.isPlinkoActive,
                is_active_yavarwee=data.miniGame.isYavarweeActive,
                is_active_coin_toss=data.miniGame.isCoinTossActive
            )
        )

    @staticmethod
    async def stage_confirm(data: StageConfirmReq):
        session = await get_session()
        await MinigameService(session).confirm_minigame(data.stageId)