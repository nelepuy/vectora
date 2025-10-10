FROM python:3.11-slim

WORKDIR /app

# Копируем только requirements сначала для кэширования слоя
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы
COPY . /app

# Используем sh -c для выполнения команд последовательно
CMD sh -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"
