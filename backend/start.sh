#!/bin/bash
set -e

echo "=== Vectora Backend Starting ==="
echo "PORT: ${PORT:-8080}"
echo "DATABASE_URL: ${DATABASE_URL:0:30}..." 

echo "🔄 Применяю миграции базы данных..."
alembic upgrade head

echo "🚀 Запускаю сервер на порту ${PORT:-8080}..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}
