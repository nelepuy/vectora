# -*- coding: utf-8 -*-
"""
Vectora Telegram Bot - Production Ready
Поддерживает работу как Mini App без локальных туннелей
"""
import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    WebAppInfo, 
    KeyboardButton, 
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    MenuButtonWebApp
)
from aiogram.filters import Command
from dotenv import load_dotenv
from pathlib import Path

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Загружаем переменные из .env
dotenv_path = Path(__file__).with_name('.env')
load_dotenv(dotenv_path=dotenv_path)

# Конфигурация из переменных окружения
TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://yourdomain.com")  # ОБЯЗАТЕЛЬНО установить в .env
API_URL = os.getenv("API_URL", "https://api.yourdomain.com")

if not TOKEN:
    raise ValueError(
        f"❌ BOT_TOKEN не найден! Проверьте файл {dotenv_path}"
    )

if not WEBAPP_URL or WEBAPP_URL == "https://yourdomain.com":
    logger.warning("⚠️ WEBAPP_URL не настроен! Установите реальный домен в .env")

logger.info(f"✅ Bot initialized with WebApp URL: {WEBAPP_URL}")

# Инициализируем бота
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    """
    Команда /start - приветствие и кнопка для открытия Mini App
    """
    user = message.from_user
    logger.info(f"User {user.id} ({user.username}) started the bot")
    
    # Создаем клавиатуру с WebApp кнопкой
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text="🚀 Открыть Vectora",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )]
        ],
        resize_keyboard=True,
        input_field_placeholder="Нажмите на кнопку ниже"
    )
    
    # Также создаем inline кнопки для альтернативного доступа
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="📱 Открыть в браузере",
                url=WEBAPP_URL
            )],
            [InlineKeyboardButton(
                text="ℹ️ Помощь",
                callback_data="help"
            )]
        ]
    )
    
    welcome_text = (
        f"👋 <b>Добро пожаловать в Vectora Task Manager!</b>\n\n"
        f"Привет, {user.first_name}! 🎯\n\n"
        f"<b>Vectora</b> - это умный планировщик задач прямо в Telegram.\n\n"
        f"<b>Возможности:</b>\n"
        f"• 📝 Создание и управление задачами\n"
        f"• 📅 Календарь задач\n"
        f"• 🏷️ Категории и теги\n"
        f"• 🔥 Приоритеты\n"
        f"• ✅ Отслеживание прогресса\n"
        f"• 🎨 Темы оформления\n\n"
        f"Нажмите кнопку <b>\"🚀 Открыть Vectora\"</b> ниже!"
    )
    
    await message.answer(
        welcome_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    
    await message.answer(
        "Или используйте кнопки:",
        reply_markup=inline_keyboard
    )


@dp.message(Command("help"))
async def help_command(message: types.Message):
    """
    Команда /help - справка по использованию
    """
    help_text = (
        "<b>📖 Справка по Vectora</b>\n\n"
        "<b>Команды:</b>\n"
        "/start - Начать работу\n"
        "/help - Эта справка\n"
        "/settings - Настройки\n\n"
        "<b>Как использовать:</b>\n"
        "1. Нажмите кнопку \"🚀 Открыть Vectora\"\n"
        "2. Создавайте задачи кнопкой ➕\n"
        "3. Организуйте задачи по категориям\n"
        "4. Отмечайте выполненные ✅\n\n"
        "<b>Поддержка:</b>\n"
        "По вопросам: @your_support"
    )
    
    await message.answer(help_text, parse_mode="HTML")


@dp.message(Command("settings"))
async def settings_command(message: types.Message):
    """
    Команда /settings - настройки
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🚀 Открыть приложение",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )],
            [InlineKeyboardButton(
                text="🔔 Уведомления",
                callback_data="notifications"
            )],
            [InlineKeyboardButton(
                text="🎨 Темы",
                callback_data="themes"
            )]
        ]
    )
    
    await message.answer(
        "<b>⚙️ Настройки</b>\n\nВыберите опцию:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@dp.callback_query(lambda c: c.data == "help")
async def help_callback(callback: types.CallbackQuery):
    """Обработка inline кнопки помощи"""
    await callback.answer()
    await help_command(callback.message)


@dp.callback_query(lambda c: c.data == "notifications")
async def notifications_callback(callback: types.CallbackQuery):
    """Обработка настроек уведомлений"""
    await callback.answer("Уведомления пока в разработке! 🔔", show_alert=True)


@dp.callback_query(lambda c: c.data == "themes")
async def themes_callback(callback: types.CallbackQuery):
    """Обработка настроек тем"""
    await callback.answer("Темы настраиваются в приложении! 🎨", show_alert=True)


@dp.message()
async def echo(message: types.Message):
    """Обработка остальных сообщений"""
    await message.answer(
        "Используйте /start для начала работы или /help для справки"
    )


async def on_startup():
    """Действия при запуске бота"""
    logger.info("🚀 Bot is starting...")
    
    # Устанавливаем Menu Button как WebApp
    try:
        await bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                text="Открыть Vectora",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        )
        logger.info("✅ Menu button set successfully")
    except Exception as e:
        logger.error(f"❌ Failed to set menu button: {e}")
    
    # Информация о боте
    me = await bot.get_me()
    logger.info(f"✅ Bot @{me.username} started successfully!")
    logger.info(f"📱 WebApp URL: {WEBAPP_URL}")
    logger.info(f"🔗 API URL: {API_URL}")


async def send_reminder(user_id: int, task_title: str, task_id: int):
    """Send task reminder to user"""
    try:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Open Task", web_app=WebAppInfo(url=f"{WEBAPP_URL}?task={task_id}"))]
        ])
        
        await bot.send_message(
            chat_id=user_id,
            text=f"⏰ Reminder: {task_title}",
            reply_markup=keyboard
        )
        logger.info(f"Reminder sent to user {user_id} for task {task_id}")
    except Exception as e:
        logger.error(f"Failed to send reminder to {user_id}: {e}")


async def on_shutdown():
    """Действия при остановке бота"""
    logger.info("⏹️ Bot is shutting down...")
    await bot.session.close()


async def main():
    """Основная функция запуска бота"""
    try:
        await on_startup()
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"❌ Error: {e}")
    finally:
        await on_shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user")
