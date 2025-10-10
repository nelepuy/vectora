FROM python:3.11-slim

# CACHEBUST для принудительной пересборки на Railway
ARG CACHEBUST=20250111_001
RUN echo "Build cache bust: $CACHEBUST"

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение
COPY . .

# CMD будет переопределён через railway.toml startCommand
