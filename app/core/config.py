from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    ENVIRONMENT: str = 'development'
    MONGO_URI: str
    DB_NAME: str
    MODEL_WEIGHTS_PATH: str
    TRACKER_CFG_PATH: str
    RTSP_URL: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()