from django.test import Client

def test_health():
    client = Client()
    url = '/minigame/health'

    response = client.get(url)

    assert response.status_code == 200
    assert response.json() == 'GOGO MiniGame Service OK'