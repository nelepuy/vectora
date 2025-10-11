FROM python:3.11-slim

WORKDIR /app

# КРИТИЧНО: CACHEBUST для принудительной пересборки на Railway
# Изменение этого ENV инвалидирует ВСЕ последующие слои Docker
ENV FORCE_REBUILD=20250111_003_FINAL_CORS_FIX

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение
COPY . .

# CMD будет переопределён через railway.toml startCommand
