from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from pydantic import Field

class Settings(BaseSettings):
    openai_api_key: str
    allowed_origins: List[str] = Field(default_factory=list)
    stockfish_path: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()