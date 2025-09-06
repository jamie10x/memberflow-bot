# backend/app/core/config.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[3]

class Settings(BaseSettings):
    # These are loaded from the .env file
    DATABASE_URL: str
    SECRET_KEY: str
    BOT_TOKEN: str
    TONCENTER_API_KEY: str

    # These have default values
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra='ignore'
    )

settings = Settings()