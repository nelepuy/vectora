#!/usr/bin/env python3
import os
import subprocess
import sys

# Отключаем буферизацию вывода
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

# Получаем PORT от Railway
port = os.getenv("PORT", "8080")

print(f"=== Vectora Backend Starting ===", flush=True)
print(f"PORT from Railway: {port}", flush=True)
print(f"DATABASE_URL: {os.getenv('DATABASE_URL', 'NOT SET')[:40]}...", flush=True)

# Применяем миграции
print("🔄 Применяю миграции...", flush=True)
result = subprocess.run(["alembic", "upgrade", "head"])
if result.returncode != 0:
    print("❌ Ошибка миграций!", flush=True)
    sys.exit(1)

# Запускаем uvicorn
print(f"🚀 Запускаю сервер на порту {port}...", flush=True)
os.execvp("uvicorn", [
    "uvicorn",
    "app.main:app",
    "--host", "0.0.0.0",
    "--port", port,
    "--forwarded-allow-ips", "*",
    "--proxy-headers"
])
