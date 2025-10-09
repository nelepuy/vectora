from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/tasks"
    APP_NAME: str = "Task Planner"
    
    class Config:
        env_file = ".env"

settings = Settings()