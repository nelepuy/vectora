# 🤖 Vectora Telegram Bot

Telegram бот для запуска Vectora Task Manager как Mini App.

## Возможности

- 🚀 Запуск Vectora Task Manager прямо из Telegram
- 📱 Работает на Desktop и Mobile
- 💬 Команды: `/start`, `/help`, `/settings`
- 🔘 Menu Button с прямым доступом к приложению
- 🎨 Inline кнопки для удобного управления
- 📊 Логирование всех действий

## Установка для разработки

### 1. Установите зависимости

```bash
pip install -r requirements.txt
```

### 2. Настройте переменные окружения

Скопируйте `.env.example` в `.env`:

```bash
cp .env.example .env
```

Отредактируйте `.env`:

```env
BOT_TOKEN=your_bot_token_from_botfather
WEBAPP_URL=http://localhost:3000
API_URL=http://localhost:8000
```

### 3. Получите токен бота

1. Откройте [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен в `.env`

### 4. Запустите бота

```bash
python bot.py
```

## Установка для продакшена

Смотрите [DEPLOYMENT.md](../DEPLOYMENT.md) для полной инструкции по развертыванию.

### Быстрый запуск через Docker

```bash
# Сборка образа
docker build -t vectora-bot .

# Запуск
docker run -d --name vectora-bot --restart unless-stopped --env-file .env vectora-bot

# Проверка логов
docker logs -f vectora-bot
```

## Настройка Bot Menu Button

После запуска бота настройте Menu Button в [@BotFather](https://t.me/BotFather):

1. `/mybots` → Выберите вашего бота
2. `Bot Settings` → `Menu Button`
3. `Configure Menu Button`
4. Введите название: **"Открыть Vectora"**
5. Введите URL: **https://vectora.yourdomain.com** (ваш production URL)

## Команды бота

- `/start` - Начать работу с ботом
- `/help` - Показать справку
- `/settings` - Открыть настройки

## Структура проекта

```
bot/
├── bot.py              # Основной файл бота
├── requirements.txt    # Python зависимости
├── Dockerfile          # Docker образ
├── .env                # Локальные переменные окружения (не коммитить!)
└── .env.example        # Пример переменных окружения
```

## Архитектура

Бот работает в режиме **long polling** (по умолчанию) или **webhook** (опционально для продакшена).

### Long Polling (по умолчанию)
- ✅ Просто настроить
- ✅ Не требует HTTPS
- ✅ Подходит для разработки
- ❌ Немного медленнее

### Webhook (для продакшена)
- ✅ Быстрее
- ✅ Меньше нагрузка на сервер
- ❌ Требует HTTPS
- ❌ Сложнее настроить

## Логирование

Бот логирует все важные события:

```
2024-01-15 10:30:45 - INFO - 🚀 Bot is starting...
2024-01-15 10:30:46 - INFO - ✅ Menu button set successfully
2024-01-15 10:30:46 - INFO - ✅ Bot @VectoraBot started successfully!
2024-01-15 10:30:46 - INFO - 📱 WebApp URL: https://vectora.example.com
2024-01-15 10:30:46 - INFO - 🔗 API URL: https://api.vectora.example.com
2024-01-15 10:31:15 - INFO - User 123456789 (john_doe) started the bot
```

## Безопасность

- ✅ Токен бота в переменных окружения (`.env`)
- ✅ `.env` в `.gitignore` - не коммитится
- ✅ Логирование действий пользователей
- ✅ Валидация URLs
- ✅ Обработка ошибок

## Troubleshooting

### Бот не отвечает

1. Проверьте токен в `.env`
2. Убедитесь, что бот запущен: `docker logs vectora-bot`
3. Проверьте интернет-соединение

### Menu Button не работает

1. Настройте Menu Button в [@BotFather](https://t.me/BotFather)
2. Убедитесь, что `WEBAPP_URL` правильный и доступен
3. ⚠️ Для продакшена ОБЯЗАТЕЛЕН HTTPS!

### "Failed to fetch" в Mini App

1. Проверьте CORS в backend (`ALLOWED_ORIGINS`)
2. Убедитесь, что backend доступен по `API_URL`
3. Проверьте SSL сертификаты (для продакшена)

## Разработка

### Локальное тестирование Mini App

Для тестирования Mini App локально используйте:

- [ngrok](https://ngrok.com/): `ngrok http 3000`
- [localtunnel](https://localtunnel.github.io/www/): `lt --port 3000`
- [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)

Затем обновите `WEBAPP_URL` в `.env`:

```env
WEBAPP_URL=https://your-tunnel-url.ngrok.io
```

### Перезапуск бота

```bash
# Docker
docker restart vectora-bot

# Локально
# Ctrl+C, затем python bot.py
```

## Полезные ссылки

- 📚 [Telegram Bot API](https://core.telegram.org/bots/api)
- 🎨 [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- 🤖 [aiogram Documentation](https://docs.aiogram.dev/)
- 🚀 [DEPLOYMENT.md](../DEPLOYMENT.md) - Полная инструкция по развертыванию

## Лицензия

См. [LICENSE](../LICENSE)
