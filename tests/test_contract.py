import pytest
from jsonschema import validate
from ai_api_testing.config import settings
from ai_api_testing.schemas import ChatCompletion


def test_status_and_content_type(basic_response):
    assert basic_response.status_code == 200
    assert "application/json" in basic_response.headers["content-type"]

def test_matches_pydantic_schema(basic_response):
    ChatCompletion.model_validate(basic_response.json())    

def test_assistant_role_and_finish_reason(basic_response):
    choice=ChatCompletion.model_validate(basic_response.json()).choices[0]
    assert choice.message.role == "assistant"
    assert choice.finish_reason in ["stop", "length"]

def test_token_uasge_adds_up(basic_response):
    usages=ChatCompletion.model_validate(basic_response.json()).usage
    assert usages.prompt_tokens > 0
    assert usages.completion_tokens > 0
    assert usages.total_tokens == usages.prompt_tokens + usages.completion_tokens

def test_response_model_matches_request(basic_response):
    assert settings.model_name in basic_response.json()["model"]


# The same contract expressed as JSON Schema (language-neutral, no Pydantic)
CHAT_SCHEMA = {
    "type": "object",
    "required": ["id", "model", "choices", "usage"],
    "properties": {
        "id": {"type": "string"},
        "model": {"type": "string"},
        "choices": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["message", "finish_reason"],
                "properties": {"message": {"type": "object", "required": ["role"]}},
            },
        },
        "usage": {
            "type": "object",
            "required": ["prompt_tokens", "completion_tokens", "total_tokens"],
        },
    },
}

def test_matches_json_schema(basic_response):
    validate(basic_response.json(),schema=CHAT_SCHEMA)