#!/bin/bash
set -e

echo "🔄 Применяю миграции базы данных..."
alembic upgrade head

echo "🚀 Запускаю сервер..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
