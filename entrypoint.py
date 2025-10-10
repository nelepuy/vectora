#!/usr/bin/env python3
import os
import sys

# Получаем порт из переменной окружения
port = os.environ.get("PORT", "8080")

# Запускаем команды
import subprocess

print("🔄 Applying migrations...")
result = subprocess.run(["alembic", "upgrade", "head"])
if result.returncode != 0:
    sys.exit(1)

print(f"🚀 Starting server on port {port}...")
subprocess.run([
    "uvicorn", 
    "app.main:app", 
    "--host", "0.0.0.0", 
    "--port", port
])
