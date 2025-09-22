# Vectora — планировщик задач (Telegram Mini App)

Коротко: мини‑приложение для Telegram. Фронтенд — React, бэкенд — FastAPI, база — PostgreSQL. Готово к локальному запуску и продакшен‑деплою.

— Backend: FastAPI, SQLAlchemy, Alembic, PostgreSQL  
— Frontend: React 18, dnd‑kit, React Big Calendar  
— Bot: Aiogram (кнопка WebApp)

## Структура

```
Vectora/
├─ backend/        # FastAPI API (app/, миграции)
├─ frontend/       # React‑клиент (src/, nginx.conf)
├─ bot/            # Telegram‑бот (aiogram)
└─ docker-compose.yml
```

## Быстрый старт (Docker)

1) Подготовьте переменные окружения (см. *.env.example):
   - backend/app/.env
   - frontend/.env
   - bot/.env
2) Запустите:

```powershell
docker-compose up -d --build
```

Доступы:
- Frontend: http://localhost:3000
- Backend API и Swagger: http://localhost:8000/docs

## Переменные окружения (основное)

Backend (`backend/app/.env`):
```
DATABASE_URL=postgresql://postgres:postgres@db:5432/tasks
JWT_SECRET=change-me
BACKEND_CORS_ORIGINS=https://your-frontend-domain.com
BACKEND_CORS_REGEX=
```

Frontend (`frontend/.env`):
```
# В проде лучше проксировать /api через тот же домен
REACT_APP_API_URL=http://localhost:8000
```

Bot (`bot/.env`):
```
TELEGRAM_BOT_TOKEN=your-telegram-bot-token   # НЕ коммитить
WEBAPP_URL=https://your-frontend-domain.com  # Публичный URL Mini App
```

## Локальная разработка (без Docker)

Backend:
```powershell
cd backend
python -m venv venv; .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend:
```powershell
cd frontend
npm install
npm start
```

Bot:
```powershell
cd bot
python bot.py
```

## Деплой и безопасность

- Настройте CORS через BACKEND_CORS_ORIGINS/BACKEND_CORS_REGEX
- В продакшене используйте домены и HTTPS (не localhost)
- Рекомендуется реверс‑прокси (Nginx), чтобы фронт ходил на `/api`
- Секреты храните только в переменных окружения/секретах CI/CD

## Лицензия

MIT