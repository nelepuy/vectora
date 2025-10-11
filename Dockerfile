FROM python:3.11-slim

WORKDIR /app

# Копируем файлы backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение из backend/
COPY backend/app ./app
COPY backend/alembic.ini .
COPY backend/migrations ./migrations

# Запускаем через alembic + uvicorn
CMD sh -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"
