from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Vectora API Minimal")

# Максимально простой CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "Vectora API работает"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/test")
def test():
    return {
        "status": "ok",
        "port": os.getenv("PORT", "unknown"),
        "database_url": os.getenv("DATABASE_URL", "not set")[:30] + "...",
    }
