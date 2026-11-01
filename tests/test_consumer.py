import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from event.consumer import consume


def test_success_commits_then_cancellation_stops_consumer():
    async def verify():
        ready = asyncio.Event()
        handled = asyncio.Event()
        stopped = asyncio.Event()

        async def handler(data):
            assert data == {'stageId': 12}
            handled.set()

        class Consumer:
            def __init__(self, *args, **kwargs):
                assert kwargs['group_id'] == 'gogo-minigame'
                assert kwargs['enable_auto_commit'] is False
                self.start = AsyncMock()
                self.commit = AsyncMock()
                self.stop = AsyncMock(side_effect=stopped.set)
                self.sent = False

            def __aiter__(self):
                return self

            async def __anext__(self):
                if not self.sent:
                    self.sent = True
                    return SimpleNamespace(topic='test', value=b'{"stageId":12}')
                await asyncio.Future()

        instance = Consumer(group_id='gogo-minigame', enable_auto_commit=False)
        with patch('event.consumer.AIOKafkaConsumer', return_value=instance), patch(
            'event.consumer.event_topic', {'test': (handler, lambda **kw: kw)}
        ):
            task = asyncio.create_task(consume(ready))
            await asyncio.wait_for(handled.wait(), timeout=1)
            assert ready.is_set()
            instance.commit.assert_awaited_once()
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            assert stopped.is_set()
            assert not ready.is_set()

    asyncio.run(verify())


def test_start_failure_clears_readiness_and_closes_consumer():
    async def verify():
        ready = asyncio.Event()
        ready.set()
        instance = SimpleNamespace(start=AsyncMock(side_effect=RuntimeError('offline')), stop=AsyncMock())
        with patch('event.consumer.AIOKafkaConsumer', return_value=instance), patch(
            'event.consumer.asyncio.sleep', new=AsyncMock(side_effect=asyncio.CancelledError)
        ):
            try:
                await consume(ready)
            except asyncio.CancelledError:
                pass
        assert not ready.is_set()
        instance.stop.assert_awaited_once()

    asyncio.run(verify())
