FROM python:3.11-slim

ARG CACHEBUST=2025-10-10-v7-simple

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# ИСПОЛЬЗУЕМ ПРОСТУЮ ВЕРСИЮ MAIN БЕЗ MIDDLEWARE
CMD uvicorn app.main_simple:app --host 0.0.0.0 --port $PORT
