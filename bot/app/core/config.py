# bot/app/core/config.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[3]

class Settings(BaseSettings):
    BOT_TOKEN: str
    BACKEND_API_URL: str
    # ADDED: The URL for our frontend Mini App
    MINI_APP_URL: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra='ignore'
    )

settings = Settings()