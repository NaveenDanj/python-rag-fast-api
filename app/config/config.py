from functools import lru_cache
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).parent.parent.parent
DEFAULT_AGENDA_PATH = str(PROJECT_ROOT / "app" / "data" / "agenda.txt")


class Settings(BaseSettings):
    openai_api_key: str = ""
    openai_base_url: str | None = None
    agenda_file_path: str = DEFAULT_AGENDA_PATH
    debug: bool = False
    gmail_username: str = ""
    gmail_app_password: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("openai_api_key", "gmail_username", "gmail_app_password", mode="before")
    @classmethod
    def normalize_secret_values(cls, value: str):
        if value is None:
            return ""

        normalized = str(value).strip()

        # Docker --env-file keeps quotes as literal characters.
        if len(normalized) >= 2 and normalized[0] == normalized[-1] and normalized[0] in {'"', "'"}:
            normalized = normalized[1:-1].strip()

        return normalized


@lru_cache()
def get_settings():
    return Settings()
