import pytest
from ai_api_testing.schemas import ErrorResponse
from ai_api_testing.config import settings

pytestmark=pytest.mark.live

GoodBody={
    "model" :settings.model_name,
    "messages":[{"role":"user","content":"hi"}],
    "max_tokens":200
}

def test_invalid_api_key_error(client):
    response=client.post("/chat/completions",json=GoodBody,
     headers={"Authorization": "invalid_api_key"})
    assert response.status_code == 401  
    ErrorResponse.model_validate(response.json())

def test_unknown_model_is_rejected(client):
    response=client.post("/chat/completions",json={**GoodBody,"model":"invalid_model"},
     headers={"Authorization": "invalid_api_key"})
    assert response.status_code == 401   
    ErrorResponse.model_validate(response.json())

def test_missing_message_model(client):
    response=client.post("/chat/completions",json={"model":settings.model_name})
    assert response.status_code == 400
    ErrorResponse.model_validate(response.json())

@pytest.mark.parametrize("bad_temp",[-1,5,"hot"])
def test_invalid_temperature_parameter(client,bad_temp):
    response=client.post("/chat/completions",json={**GoodBody,"temperature":bad_temp})
    assert response.status_code == 400
    ErrorResponse.model_validate(response.json())