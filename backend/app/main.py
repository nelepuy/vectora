from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import tasks
from app.settings import settings

APP_NAME = settings.app_name
APP_VERSION = settings.app_version

app = FastAPI(title=APP_NAME, version=APP_VERSION)

# Преобразуем CORS-оригины к списку строк (в .env может быть одна строка или JSON-массив)
origins_setting = settings.backend_cors_origins
if isinstance(origins_setting, str):
    allow_origins = [o.strip() for o in origins_setting.split(",") if o.strip()]
else:
    allow_origins = origins_setting or []

# CORS: в проде домены задаются через переменные окружения
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
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