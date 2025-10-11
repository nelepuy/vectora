FROM python:3.11-slim

# КРИТИЧНО: Инвалидируем Docker кэш через изменение layer order
RUN echo "FORCE REBUILD: 2025-01-11T00:06:00Z" > /tmp/rebuild.txt && cat /tmp/rebuild.txt

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение
COPY . .

# CMD будет переопределён через railway.toml startCommand
