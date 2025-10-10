from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.routers import tasks, auth
from app.settings import settings
from app.exceptions import VectoraException
from app.logging_config import logger
from app.security import SecurityHeaders
import time

APP_NAME = settings.app_name
APP_VERSION = settings.app_version

# Rate limiter для защиты от DDoS
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Vectora Task Manager API — система управления задачами для Telegram Mini App",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Добавляем rate limiter в state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Преобразуем CORS-оригины к списку строк (в .env может быть одна строка или JSON-массив)
origins_setting = settings.backend_cors_origins
if isinstance(origins_setting, str):
    allow_origins = [o.strip() for o in origins_setting.split(",") if o.strip()]
else:
    allow_origins = origins_setting or []

# CORS: ВРЕМЕННО открыты все origins для тестирования Railway
# ВАЖНО: CORS middleware должен быть ПЕРВЫМ, чтобы заголовки добавлялись даже при ошибках!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ВРЕМЕННО: разрешаем все origins
    allow_credentials=False,  # Должно быть False когда allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
)


# Middleware для добавления security headers
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    
    # Добавляем security headers
    security_headers = SecurityHeaders.get_secure_headers()
    for header, value in security_headers.items():
        response.headers[header] = value
    
    return response


# Middleware для логирования запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Логируем IP для отслеживания подозрительной активности
    client_host = request.client.host if request.client else "unknown"
    logger.info(f"Запрос: {request.method} {request.url.path} от {client_host}")
    
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

# Trusted Host Middleware - защита от Host header attacks
# ОТКЛЮЧЕНО для Railway, так как Railway использует внутренний прокси
# if not settings.debug:
#     app.add_middleware(
#         TrustedHostMiddleware,
#         allowed_hosts=["localhost", "127.0.0.1", "*.railway.app", "*.up.railway.app"]
#     )

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(tasks.router)


@app.on_event("startup")
async def startup_event():
    """Действия при запуске приложения."""
    logger.info(f"{APP_NAME} v{APP_VERSION} запускается...")
    logger.info(f"Режим отладки: {settings.debug}")
    logger.info(f"CORS Origins: {allow_origins}")
    logger.info(f"Database URL: {settings.database_url[:30]}...")


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