FROM python:3.11-slim@sha256:5e9093a415c674b51e705d42dde4dd6aad8c132dab6ca3e81ecd5cbbe3689bd2

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# КРИТИЧНО: Инвалидируем кэш ПЕРЕД копированием кода
RUN echo "INVALIDATE_CACHE_NOW=$(date +%s)" > /tmp/cachebust.txt && cat /tmp/cachebust.txt

# Копируем приложение (это НЕ будет cached благодаря RUN выше)
COPY . .

# CMD будет переопределён через railway.toml startCommand
