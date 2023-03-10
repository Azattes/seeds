from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    database_url: str
    is_test: bool = False

    class Config:
        env_file = BASE_DIR / ".env"
