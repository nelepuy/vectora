from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
import secrets


class Settings(BaseSettings):
    app_name: str = "Vectora API"
    app_version: str = "1.0.0"
    debug: bool = False

    secret_key: str = secrets.token_urlsafe(32)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000

    backend_cors_origins: Optional[str] = "http://localhost:3000,http://localhost:8000,https://nelepuy.github.io"
    backend_cors_regex: Optional[str] = None
    
    telegram_bot_token: Optional[str] = None
    database_url: str = "postgresql://postgres:postgres@db:5432/tasks"
    
    password_min_length: int = 8
    password_require_uppercase: bool = False
    password_require_lowercase: bool = True
    password_require_digit: bool = True
    password_require_special: bool = False
    
    session_timeout_minutes: int = 60
    max_login_attempts: int = 5
    lockout_duration_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
