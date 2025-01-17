from rest_framework.test import APIClient


def test_health():
    client = APIClient()
    url = '/health'

    response = client.get(url)

    assert response.status_code == 200