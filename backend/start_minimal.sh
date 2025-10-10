#!/bin/bash
set -e

echo "=== MINIMAL VECTORA START ==="
echo "PORT: ${PORT:-8080}"

# Без миграций - просто запуск
exec uvicorn app.main_minimal:app --host 0.0.0.0 --port ${PORT:-8080}
