from pydantic import BaseModel, ConfigDict


class Message(BaseModel):
    model_config = ConfigDict(extra="ignore")
    role: str
    content: str | None = None


class Choice(BaseModel):
    model_config = ConfigDict(extra="ignore")
    index: int
    message: Message          # was "Message" (capitalised) — API sends "message"
    finish_reason: str | None


class Usage(BaseModel):
    model_config = ConfigDict(extra="ignore")
    prompt_tokens: int        # was "prompt_token"
    completion_tokens: int    # was "Completion_token"
    total_tokens: int         # was "total_token"


class ChatCompletion(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    object: str
    created: int
    model: str
    choices: list[Choice]
    usage: Usage


class ErrorBody(BaseModel):
    model_config = ConfigDict(extra="ignore")
    message: str
    type: str | None = None


class ErrorResponse(BaseModel):
    error: ErrorBody
