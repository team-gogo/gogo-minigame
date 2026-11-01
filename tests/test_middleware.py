import asyncio
import logging
import re

import pytest
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse, Response, StreamingResponse
from fastapi.testclient import TestClient

from middleware import LoggingMiddleware


LOGGER_NAME = 'GOGO-MiniGame Logger'


def logged_messages(caplog):
    return [record.getMessage() for record in caplog.records if record.name == LOGGER_NAME]


def test_request_and_response_secrets_are_not_logged_and_endpoint_receives_body(caplog):
    app = FastAPI()
    app.add_middleware(LoggingMiddleware)
    body = b'{"token":"private-request-body"}'

    @app.post('/minigame/play', status_code=201)
    async def play(request: Request):
        assert request.headers['authorization'] == 'Bearer private-header'
        assert request.cookies['session'] == 'private-cookie'
        assert request.query_params['token'] == 'private-query'
        assert await request.body() == body
        return {'token': 'private-response-body'}

    with TestClient(app) as client, caplog.at_level(logging.INFO, logger=LOGGER_NAME):
        response = client.post(
            '/minigame/play?token=private-query',
            content=body,
            headers={
                'Authorization': 'Bearer private-header',
                'Cookie': 'session=private-cookie',
                'Content-Type': 'application/json',
            },
        )

    assert response.status_code == 201
    assert response.json() == {'token': 'private-response-body'}
    messages = logged_messages(caplog)
    assert len(messages) == 1
    assert re.fullmatch(
        r'Log-ID: [0-9a-f-]{36}, Method: POST, Path: /minigame/play, '
        r'Status-Code: 201, Response Time: \d+\.\d{2}ms',
        messages[0],
    )
    assert not any(
        secret in messages[0]
        for secret in ('private-header', 'private-cookie', 'private-query',
                       'private-request-body', 'private-response-body')
    )
    assert not any(label in messages[0] for label in ('Headers:', 'Content-Type:', 'Params:', 'Body:'))


@pytest.mark.parametrize('path', [
    '/minigame/health',
    '/minigame/health/readiness',
    '/favicon.ico',
    '/actuator/prometheus',
])
def test_health_and_metrics_paths_are_not_logged(path, caplog):
    app = FastAPI()
    app.add_middleware(LoggingMiddleware)
    app.add_api_route(path, lambda: PlainTextResponse('ok'))

    with TestClient(app) as client, caplog.at_level(logging.INFO, logger=LOGGER_NAME):
        response = client.get(path)

    assert response.text == 'ok'
    assert logged_messages(caplog) == []


@pytest.mark.parametrize('response_factory,expected', [
    (lambda: PlainTextResponse('private-plain-text', status_code=202, headers={'X-Marker': 'private-header'}),
     b'private-plain-text'),
    (lambda: Response(b'\x00\xffprivate-binary', media_type='application/octet-stream',
                      status_code=202, headers={'X-Marker': 'private-header'}),
     b'\x00\xffprivate-binary'),
])
def test_non_json_responses_are_unchanged(response_factory, expected, caplog):
    app = FastAPI()
    app.add_middleware(LoggingMiddleware)
    app.add_api_route('/minigame/payload', response_factory)

    with TestClient(app) as client, caplog.at_level(logging.INFO, logger=LOGGER_NAME):
        response = client.get('/minigame/payload')

    assert response.status_code == 202
    assert response.headers['x-marker'] == 'private-header'
    assert response.content == expected
    assert len(logged_messages(caplog)) == 1
    assert 'Status-Code: 202' in logged_messages(caplog)[0]
    assert 'private-' not in logged_messages(caplog)[0]


def test_streaming_response_is_not_consumed_or_replaced(caplog):
    async def verify():
        generated = []

        async def chunks():
            generated.append('first')
            yield b'private-stream-body'
            generated.append('second')
            yield b'\x00\xff'

        iterator = chunks()
        response = StreamingResponse(iterator, status_code=202, headers={'X-Marker': 'private-stream-header'})
        request = Request({
            'type': 'http', 'method': 'GET', 'path': '/minigame/stream',
            'query_string': b'', 'headers': [],
        })

        async def call_next(received):
            assert received is request
            return response

        result = await LoggingMiddleware(FastAPI()).dispatch(request, call_next)
        assert result is response
        assert result.body_iterator is iterator
        assert generated == []
        assert b''.join([chunk async for chunk in result.body_iterator]) == b'private-stream-body\x00\xff'
        assert generated == ['first', 'second']

    with caplog.at_level(logging.INFO, logger=LOGGER_NAME):
        asyncio.run(verify())

    assert len(logged_messages(caplog)) == 1
    assert 'private-stream' not in logged_messages(caplog)[0]


def test_handled_error_logs_actual_status_without_response_details(caplog):
    app = FastAPI()
    app.add_middleware(LoggingMiddleware)

    @app.get('/minigame/rejected')
    async def rejected():
        raise HTTPException(status_code=403, detail='private-error-detail')

    with TestClient(app) as client, caplog.at_level(logging.INFO, logger=LOGGER_NAME):
        response = client.get('/minigame/rejected')

    assert response.status_code == 403
    assert response.json() == {'detail': 'private-error-detail'}
    assert len(logged_messages(caplog)) == 1
    assert 'Status-Code: 403' in logged_messages(caplog)[0]
    assert 'private-error-detail' not in logged_messages(caplog)[0]


def test_unhandled_exception_propagates_without_false_success_log(caplog):
    app = FastAPI()
    app.add_middleware(LoggingMiddleware)
    error = RuntimeError('private-exception-detail')

    @app.get('/minigame/failure')
    async def failure():
        raise error

    with TestClient(app) as client, caplog.at_level(logging.INFO, logger=LOGGER_NAME):
        with pytest.raises(RuntimeError) as caught:
            client.get('/minigame/failure')

    assert caught.value is error
    assert logged_messages(caplog) == []
