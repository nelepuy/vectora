#!/usr/bin/env python3
import os
import subprocess
import sys

# Получаем PORT от Railway
port = os.getenv("PORT", "8080")

print(f"=== Vectora Backend Starting ===")
print(f"PORT from Railway: {port}")
print(f"DATABASE_URL: {os.getenv('DATABASE_URL', 'NOT SET')[:40]}...")

# Применяем миграции
print("🔄 Применяю миграции...")
result = subprocess.run(["alembic", "upgrade", "head"])
if result.returncode != 0:
    print("❌ Ошибка миграций!")
    sys.exit(1)

# Запускаем uvicorn
print(f"🚀 Запускаю сервер на порту {port}...")
os.execvp("uvicorn", [
    "uvicorn",
    "app.main:app",
    "--host", "0.0.0.0",
    "--port", port
])
