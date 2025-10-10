FROM python:3.11-slim

# ФОРСИРУЕМ ПОЛНУЮ ПЕРЕСБОРКУ
ARG CACHEBUST=final-rebuild-171920-no-cache

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# ПРОСТАЯ ВЕРСИЯ БЕЗ ВСЕХ MIDDLEWARE
CMD ["uvicorn", "app.main_simple:app", "--host", "0.0.0.0", "--port", "8080"]
