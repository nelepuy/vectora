FROM python:3.11-slim@sha256:5e9093a415c674b51e705d42dde4dd6aad8c132dab6ca3e81ecd5cbbe3689bd2

# КРИТИЧНО: Инвалидируем Docker кэш через изменение layer order + timestamp в ENV
ENV CACHEBUST_TIMESTAMP="2025-01-11T00:09:00Z" \
    FORCE_REBUILD="TRUE"
RUN echo "Building at: $CACHEBUST_TIMESTAMP" && \
    echo "Force rebuild: $FORCE_REBUILD"

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение
COPY . .

# CMD будет переопределён через railway.toml startCommand
