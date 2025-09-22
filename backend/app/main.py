from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import tasks
from app.settings import settings

APP_NAME = settings.app_name
APP_VERSION = settings.app_version

app = FastAPI(title=APP_NAME, version=APP_VERSION)

# CORS: в проде домены задаются через переменные окружения
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins or [],
    allow_origin_regex=settings.backend_cors_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(tasks.router)


@app.get("/health")
def health() -> dict:
    """Проверка доступности сервиса (healthcheck)."""
    return {"status": "ok"}


@app.get("/version")
def version() -> dict:
    """Текущая версия сервиса."""
    return {"name": APP_NAME, "version": APP_VERSION}


@app.get("/")
def root() -> dict:
    """Простой ответ для проверки запуска."""
    return {"message": f"{APP_NAME} запущен", "version": APP_VERSION}