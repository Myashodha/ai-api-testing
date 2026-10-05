import pytest
from ai_api_testing.config import settings


@pytest.mark.live
def test_smoke(client):
    response=client.post("/chat/completions",json={
        "model": settings.model_name,
        "messages":[{"role":"user","content":"Say hello with one word"}],
        "temperature":0,
        "max_tokens":200
    })

    print(response.status_code)
    print(response.text)
