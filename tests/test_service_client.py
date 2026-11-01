import asyncio
from unittest.mock import patch

import httpx
import pytest
from fastapi import HTTPException

from service_client import get_service_text


def run_request(handler, service="gogo-user", path="/user/student?userId=42"):
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    with patch("service_client.httpx.AsyncClient", return_value=client):
        return asyncio.run(get_service_text(service, path))


def test_service_dns_preserves_query():
    def handler(request):
        assert request.url.host == "gogo-user.gogo.svc.cluster.local"
        assert request.url.params["userId"] == "42"
        return httpx.Response(200, json={"studentId": 123})

    assert '"studentId":123' in run_request(handler)


def test_url_override(monkeypatch):
    monkeypatch.setenv("USER_SERVICE_URL", "http://user.test:8081")

    def handler(request):
        assert request.url.host == "user.test"
        assert request.url.port == 8081
        return httpx.Response(200, text="ok")

    assert run_request(handler) == "ok"


@pytest.mark.parametrize("status", [301, 403, 500])
def test_upstream_errors_are_not_exposed(status):
    with pytest.raises(HTTPException) as caught:
        run_request(lambda request: httpx.Response(status, text="sensitive response"))
    assert caught.value.status_code == 502
    assert "sensitive" not in caught.value.detail


def test_timeout():
    def handler(request):
        raise httpx.ReadTimeout("timeout", request=request)

    with pytest.raises(HTTPException) as caught:
        run_request(handler)
    assert caught.value.status_code == 504


@pytest.mark.parametrize("service,path", [
    ("unknown", "/path"),
    ("gogo-user", "//attacker.test/path"),
    ("gogo-user", "https://attacker.test/path"),
])
def test_invalid_destinations(service, path):
    with pytest.raises(ValueError):
        asyncio.run(get_service_text(service, path))
