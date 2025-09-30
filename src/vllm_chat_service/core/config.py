from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App configuration loaded from environment vars or .env file."""

    VLLM_URL: str = "http://127.0.0.1:8000/v1"  # Base URL for vLLM API
    MODEL_ID: str = (
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Model ID as specified in README
    )
    LOG_LEVEL: str = "INFO"  # Logging

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
