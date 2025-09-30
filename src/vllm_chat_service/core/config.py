from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    VLLM_URL: str = "http://127.0.0.1:8000/v1"
    MODEL_ID: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    LOG_LEVEL: str = "INFO"
    VLLM_USE_V1: int = 0

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
