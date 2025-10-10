FROM python:3.11-slim

# НОВЫЙ CACHEBUST ДЛЯ НОВОГО СЕРВИСА
ARG CACHEBUST=new-service-20251010-173950

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . /app

# ЗАПУСК MAIN_SIMPLE БЕЗ MIDDLEWARE
CMD uvicorn app.main_simple:app --host 0.0.0.0 --port 8080
