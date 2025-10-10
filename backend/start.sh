#!/bin/bash
set -e

echo "🔄 Применяю миграции базы данных..."
alembic upgrade head

echo "🚀 Запускаю сервер..."
if [ -z "$PORT" ]; then
  PORT=8000
fi
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
