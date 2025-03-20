from fastapi.testclient import TestClient

from server import app


def test_health():
    client = TestClient(app)
    response = client.get('/minigame/health')
    assert response.status_code == 200
    assert response.json() == 'GOGO Minigame Service OK'