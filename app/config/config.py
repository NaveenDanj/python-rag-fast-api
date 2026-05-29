from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
PROJECT_ROOT = Path(__file__).parent.parent.parent
DEFAULT_AGENDA_PATH = str(PROJECT_ROOT / "app" / "data" / "agenda.txt")

class Settings(BaseSettings):
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    agenda_file_path: str = os.getenv("AGENDA_FILE_PATH", DEFAULT_AGENDA_PATH)
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    gmail_username: str = os.getenv("GMAIL_USERNAME", "")
    gmail_app_password: str = os.getenv("GMAIL_APP_PASSWORD", "")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


@lru_cache()
def get_settings():
    return Settings()
