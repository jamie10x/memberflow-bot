# backend/app/core/config.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Define the project's root directory.
# `Path(__file__).resolve()` gets the absolute path to this file.
# `.parents[3]` goes up 3 levels from `.../backend/app/core/` to the project root.
BASE_DIR = Path(__file__).resolve().parents[3]

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra='ignore'
    )

# Create a single, reusable instance of the settings
settings = Settings()