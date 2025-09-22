# -*- coding: utf-8 -*-
import asyncio
import os
import subprocess
import re
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from dotenv import load_dotenv
from pathlib import Path

# Загружаем переменные из .env, расположенного рядом с этим файлом
dotenv_path = Path(__file__).with_name('.env')
load_dotenv(dotenv_path=dotenv_path)

# Читаем токен из окружения/файла .env
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError(
        f"Не найден TELEGRAM_BOT_TOKEN. Проверьте файл {dotenv_path} или переменные окружения."
    )

def get_tunnel_url():
    try:
        lt_path = os.path.expanduser("~\\AppData\\Roaming\\npm\\lt.cmd")
        process = subprocess.Popen(
            [lt_path, "--port", "3000", "--subdomain", "vectora-tasks"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Ждем URL не более 10 секунд
        for _ in range(10):
            line = process.stdout.readline()
            if not line:
                break
            if "your url is:" in line:
                url = re.search(r"your url is: (https://[\w\-.]+\.loca\.lt)", line)
                if url:
                    print(f"LocalTunnel запущен на {url.group(1)}")
                    return url.group(1)
        
        # Если URL не получен, завершаем процесс
        process.terminate()
        print("Не удалось получить URL от LocalTunnel")
        return None
    except Exception as e:
        print(f"Ошибка LocalTunnel: {e}")
        return None

# URL Mini App: в продакшене ОБЯЗАТЕЛЬНО задать WEBAPP_URL (например, https://app.yourdomain.com)
WEBAPP_URL = os.getenv("WEBAPP_URL") or get_tunnel_url() or ""
if not WEBAPP_URL:
    print("Внимание: WEBAPP_URL не задан. Кнопка WebApp не будет работать вне разработки.")

# Инициализируем бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Открыть планер", web_app=WebAppInfo(url=WEBAPP_URL))]
        ],
        resize_keyboard=True
    )
    await message.answer("Добро пожаловать! Откройте планер задач:", reply_markup=keyboard)

@dp.message()
async def echo(message: types.Message):
    await message.answer("Используйте /start для начала работы")

async def main():
    print("Запускаем бота...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
