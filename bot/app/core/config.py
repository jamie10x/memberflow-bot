# bot/app/core/config.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Define the project's root directory.
# `Path(__file__).resolve()` gets the absolute path to this file.
# `.parents[3]` goes up 3 levels from `.../bot/app/core/` to the project root.
BASE_DIR = Path(__file__).resolve().parents[3]

class Settings(BaseSettings):
    BOT_TOKEN: str

    # URL for our backend API
    BACKEND_API_URL: str = "http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra='ignore'
    )

settings = Settings()