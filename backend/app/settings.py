from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional


class Settings(BaseSettings):
    app_name: str = "Vectora API"
    app_version: str = "1.0.0"
    
    # Режим отладки (отключает некоторые проверки безопасности)
    debug: bool = False

    # CORS
    # Читаем как строку (список доменов через запятую), парсим вручную в main.py
    backend_cors_origins: Optional[str] = None
    backend_cors_regex: Optional[str] = None
    
    # Telegram
    telegram_bot_token: Optional[str] = None
    
    # База данных
    database_url: str = "postgresql://postgres:postgres@db:5432/tasks"

    # Конфигурация Settings для pydantic-settings
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
