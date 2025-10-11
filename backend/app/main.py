from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from app.routers import tasks, auth, stats
from app.settings import settings
from app.exceptions import VectoraException
from app.logging_config import logger
from app.security import SecurityHeaders
import time

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Vectora Task Manager API",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None
)

origins_setting = settings.backend_cors_origins
if isinstance(origins_setting, str):
    allow_origins = [o.strip() for o in origins_setting.split(",") if o.strip()]
else:
    allow_origins = origins_setting or []


@app.middleware("http")
async def add_cors_and_security_headers(request: Request, call_next):
    if request.method == "OPTIONS":
        response = JSONResponse(content={}, status_code=200)
    else:
        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            response = JSONResponse(
                content={"detail": "Internal server error"},
                status_code=500
            )
    
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Max-Age"] = "600"
    
    security_headers = SecurityHeaders.get_secure_headers()
    for header, value in security_headers.items():
        response.headers[header] = value
    
    return response


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    client_host = request.client.host if request.client else "unknown"
    logger.info(f"{request.method} {request.url.path} from {client_host}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"Response {response.status_code} in {process_time:.3f}s")
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Error: {str(e)} after {process_time:.3f}s")
        raise


@app.exception_handler(VectoraException)
async def vectora_exception_handler(request: Request, exc: VectoraException):
    logger.warning(f"Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(stats.router)


@app.on_event("startup")
async def startup_event():
    logger.info(f"{settings.app_name} v{settings.app_version} started")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"CORS origins: {allow_origins}")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"{settings.app_name} shutting down")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/version")
def version() -> dict:
    return {"name": settings.app_name, "version": settings.app_version}


@app.get("/")
def root() -> dict:
    return {"message": f"{settings.app_name} API", "version": settings.app_version}