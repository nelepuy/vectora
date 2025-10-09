from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
import secrets


class Settings(BaseSettings):
    app_name: str = "Vectora API"
    app_version: str = "1.0.0"
    
    # Режим отладки (отключает некоторые проверки безопасности)
    debug: bool = False

    # Security - ОБЯЗАТЕЛЬНО устанавливать через переменные окружения!
    secret_key: str = secrets.token_urlsafe(32)  # Генерируется автоматически, но ДОЛЖЕН быть в .env
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000

    # CORS - строгие настройки для продакшна
    backend_cors_origins: Optional[str] = "http://localhost:3000,http://localhost:8000"
    backend_cors_regex: Optional[str] = None
    
    # Telegram
    telegram_bot_token: Optional[str] = None
    
    # База данных
    database_url: str = "postgresql://postgres:postgres@db:5432/tasks"
    
    # Security settings
    password_min_length: int = 8
    password_require_uppercase: bool = False
    password_require_lowercase: bool = True
    password_require_digit: bool = True
    password_require_special: bool = False
    
    # Session settings
    session_timeout_minutes: int = 60
    max_login_attempts: int = 5
    lockout_duration_minutes: int = 30

    # Конфигурация Settings для pydantic-settings
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
