from pydantic import BaseSettings, AnyHttpUrl
from typing import List, Optional


class Settings(BaseSettings):
    app_name: str = "Vectora API"
    app_version: str = "1.0.0"

    # CORS
    backend_cors_origins: List[AnyHttpUrl] = []  # comma-separated in env
    backend_cors_regex: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
