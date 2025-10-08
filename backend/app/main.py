from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routers import tasks
from app.settings import settings
from app.exceptions import VectoraException
from app.logging_config import logger
import time

APP_NAME = settings.app_name
APP_VERSION = settings.app_version

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Vectora Task Manager API — система управления задачами для Telegram Mini App",
    docs_url="/docs",
    redoc_url="/redoc"
)


# Middleware для логирования запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    logger.info(f"Запрос: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"Ответ: {response.status_code} за {process_time:.3f}s")
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Ошибка: {str(e)} за {process_time:.3f}s")
        raise


# Обработчик исключений приложения
@app.exception_handler(VectoraException)
async def vectora_exception_handler(request: Request, exc: VectoraException):
    logger.warning(f"Обработано исключение: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

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


@app.on_event("startup")
async def startup_event():
    """Действия при запуске приложения."""
    logger.info(f"{APP_NAME} v{APP_VERSION} запускается...")
    logger.info(f"Режим отладки: {settings.debug}")


@app.on_event("shutdown")
async def shutdown_event():
    """Действия при остановке приложения."""
    logger.info(f"{APP_NAME} останавливается...")


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