from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):

    model_config=SettingsConfigDict(env_file=".env")
    groq_api_key:str
    model_name: str = "openai/gpt-oss-120b"
    base_url: str="https://api.groq.com/openai/v1"
    timeout_seconds: float=30.0


settings= Settings()
