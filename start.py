#!/usr/bin/env python3
"""Скрипт запуска сервера с применением миграций"""
import os
import subprocess
import sys

def main():
    print("🔄 Применяю миграции базы данных...")
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("✅ Миграции применены успешно")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при применении миграций: {e}")
        sys.exit(1)
    
    print("🚀 Запускаю сервер...")
    port = os.environ.get("PORT", "8080")
    
    # Запускаем uvicorn
    subprocess.run([
        "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", port
    ])

if __name__ == "__main__":
    main()
