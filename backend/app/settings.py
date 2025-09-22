from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional


class Settings(BaseSettings):
    app_name: str = "Vectora API"
    app_version: str = "1.0.0"

    # CORS
    # В Pydantic v2 списки из env по умолчанию парсятся через JSON. Проще задавать как строки через запятую и парсить вручную,
    # но для краткости оставим List[str] и будем указывать в .env один домен либо JSON-массив.
    backend_cors_origins: List[str] = []
    backend_cors_regex: Optional[str] = None

    # Конфигурация Settings для pydantic-settings
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
