# Vectora - Telegram Mini App Task Manager# 📋 Vectora — Telegram Mini App Task Manager



Task management application built as a Telegram Mini App.Modern task manager as a Telegram Mini App with FastAPI backend and React frontend.



## Stack## ✨ Возможности



- **Backend:** FastAPI, PostgreSQL, SQLAlchemy, Alembic### Основные

- **Frontend:** React 18, Telegram WebApp SDK- 📝 **CRUD операции** для задач с полной валидацией

- **Bot:** Aiogram 3- 🔍 **Фильтрация и поиск** по статусу, приоритету, тексту (debounced)

- **Deployment:** Docker Compose- 📅 **Календарное представление** (React Big Calendar)

- 📊 **Dashboard со статистикой**: completion rate, приоритеты, overdue задачи

## Quick Start- 🎨 **Тёмная/светлая тема** с синхронизацией Telegram theme

- 📱 **Адаптивный дизайн** для всех устройств

```bash

# 1. Setup environment### Технические

cp backend/.env.example backend/.env- 🔐 **Telegram WebApp Authentication** (HMAC-SHA256 validation)

cp frontend/.env.example frontend/.env- ✅ **Comprehensive Testing** (pytest, 85%+ coverage, unit + integration)

cp bot/.env.example bot/.env- 📝 **Structured Logging** с request/response tracking

- 🚀 **CI/CD Pipeline** (GitHub Actions: тесты, lint, build)

# 2. Add your Telegram bot token to bot/.env- 🐳 **Docker контейнеризация** (production-ready compose)

TELEGRAM_BOT_TOKEN=your_token_here- 📚 **API Documentation** (OpenAPI/Swagger, Postman collection)



# 3. Start services## 🏗️ Архитектура

docker-compose up -d --build

**Backend:** FastAPI, SQLAlchemy, Alembic, PostgreSQL  

# 4. Apply migrations**Frontend:** React 18, Custom hooks, CSS animations  

docker exec vectora-backend-1 alembic upgrade head**Bot:** Aiogram (WebApp button)  

**Testing:** pytest, pytest-cov, httpx TestClient  

# 5. Access**CI/CD:** GitHub Actions, Docker, Nginx

# - Frontend: http://localhost:3000

# - Backend API: http://localhost:8000## 📁 Структура проекта

# - API Docs: http://localhost:8000/docs

``````

Vectora/

## Project Structure├─ backend/              # FastAPI REST API

│  ├─ app/

```│  │  ├─ main.py         # Application entry point с middleware

vectora/│  │  ├─ auth.py         # Telegram WebApp authentication

├── backend/          # FastAPI application│  │  ├─ crud.py         # Database operations с filtering

│   ├── app/│  │  ├─ models.py       # SQLAlchemy models

│   │   ├── main.py          # App entry point│  │  ├─ schemas.py      # Pydantic schemas (v2)

│   │   ├── models.py        # Database models│  │  ├─ exceptions.py   # Centralized error handling

│   │   ├── schemas.py       # Pydantic schemas│  │  └─ routers/        # API endpoints

│   │   ├── crud.py          # Database operations│  ├─ tests/             # pytest test suite (85%+ coverage)

│   │   └── routers/         # API routes│  ├─ migrations/        # Alembic database migrations

│   ├── tests/               # pytest tests│  └─ API.md             # Comprehensive API documentation

│   └── migrations/          # Alembic migrations│

│├─ frontend/             # React SPA

├── frontend/         # React application│  ├─ src/

│   └── src/│  │  ├─ components/

│       ├── components/      # React components│  │  │  ├─ TaskList.jsx     # Task management

│       └── hooks/           # Custom hooks│  │  │  ├─ TaskFilters.jsx  # Search & filtering (debounced)

││  │  │  ├─ TaskStats.jsx    # Dashboard statistics

├── bot/              # Telegram bot│  │  │  └─ CalendarView.jsx # Calendar interface

│   └── bot.py               # Bot logic│  │  └─ hooks/

││  │     └─ useTelegramWebApp.js

└── docker-compose.yml       # Docker services│  └─ Dockerfile

```│

├─ bot/                  # Telegram Bot (aiogram)

## Development│  └─ bot.py             # WebApp button handler

│

### Backend├─ .github/

│  ├─ workflows/         # CI/CD pipelines

```bash│  │  ├─ backend-tests.yml

cd backend│  │  ├─ frontend-lint.yml

python -m venv venv│  │  └─ docker-build.yml

source venv/bin/activate  # or .\venv\Scripts\activate on Windows│  ├─ ISSUE_TEMPLATE/    # Bug & feature templates

pip install -r requirements.txt│  └─ PULL_REQUEST_TEMPLATE.md

uvicorn app.main:app --reload│

```├─ CONTRIBUTING.md       # Contribution guidelines

├─ DEPLOYMENT.md         # Production deployment guide

### Frontend├─ ROADMAP.md            # Development roadmap 2025

└─ docker-compose.yml    # Local development setup

```bash```

cd frontend

npm install## 🚀 Быстрый старт

npm start

```### 🏠 Локальный запуск (бесплатно, 5 минут)



### Bot```powershell

# Автоматический запуск всего проекта

```bash.\start.ps1

cd bot```

python bot.py

```Скрипт автоматически:

- ✅ Проверит Docker и конфигурацию

## Testing- ✅ Запустит все контейнеры (Backend, Frontend, Bot, PostgreSQL)

- ✅ Применит миграции БД

```bash- ✅ Настроит HTTPS туннель (localtunnel, работает в России)

cd backend- ✅ Покажет инструкции для @BotFather

pytest tests/ -v --cov=app

```**Готово!** Откройте бота в Telegram → `/start` → Нажмите кнопку "Открыть Vectora"



## Telegram Mini App Setup---



1. Create bot with @BotFather### ☁️ Деплой в продакшн (GitHub Student Pack)

2. Get bot token and add to `bot/.env`

3. For local development, use ngrok or localtunnel:**Рекомендуем:** Railway + GitHub Pages ⭐

   ```bash

   npx localtunnel --port 3000```powershell

   ```# Автоматический деплой на Railway + GitHub Pages

4. Set Menu Button in @BotFather with your HTTPS URL.\deploy-railway.ps1

```

## Environment Variables

**Что получите:**

**backend/.env:**- 🚄 **Backend + Bot** на Railway (~$5/мес)

```env- � **Frontend** на GitHub Pages (БЕСПЛАТНО)

DATABASE_URL=postgresql://postgres:postgres@db:5432/tasks- 🎓 **GitHub Student Pack** покрывает все расходы ($100 + $5/мес)

SECRET_KEY=your-secret-key- 🇷🇺 **Работает в России** без VPN

TELEGRAM_BOT_TOKEN=your-bot-token- � **Авто-деплой** через GitHub Actions

```

**Альтернативы:**

**frontend/.env:**```powershell

```env# Локально — бесплатно навсегда

REACT_APP_API_URL=http://localhost:8000.\start.ps1

``````



**bot/.env:**📚 **Полная документация:**

```env- [Railway + GitHub Pages](./DEPLOYMENT_RAILWAY_PAGES.md) ⭐ Рекомендуем

TELEGRAM_BOT_TOKEN=your-bot-token- [Все варианты деплоя](./DEPLOYMENT_OPTIONS_RU.md)

WEBAPP_URL=https://your-app-url.com- [GitHub Student Pack](https://education.github.com/pack) — получите бонусы

```

### 🚀 Production развертывание

## API Documentation

Для полного production деплоя на VPS с HTTPS и интеграцией в Telegram смотрите **[DEPLOYMENT.md](DEPLOYMENT.md)** - пошаговая инструкция включает:

Once running, visit:

- Swagger UI: http://localhost:8000/docs✅ Настройку VPS (Ubuntu/Debian)  

- ReDoc: http://localhost:8000/redoc✅ SSL сертификаты (Let's Encrypt)  

✅ Nginx reverse proxy  

## License✅ Telegram Mini App интеграцию  

✅ Docker production setup  

MIT✅ Мониторинг и резервное копирование  

✅ Security checklist

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

## 🧪 Тестирование

### Backend тесты

```powershell
cd backend
pytest tests/ -v --cov=app --cov-report=html
```

**Test Coverage:**
- ✅ Authentication (Telegram initData validation)
- ✅ CRUD operations (create, read, update, delete)
- ✅ Filtering & search (status, priority, text search)
- ✅ Pagination (skip/limit)
- ✅ User isolation (multi-tenant security)
- ✅ Integration tests (full API flow)

### CI/CD

GitHub Actions автоматически запускает:
- Backend тесты с PostgreSQL
- Frontend lint & build
- Docker image builds
- Coverage reporting

## 📚 Документация

- **[Quick Start (RU)](QUICK_START_RU.md)** - быстрый старт на русском (5 минут)
- **[API Documentation](backend/API.md)** - описание REST API endpoints
- **[Contributing Guide](CONTRIBUTING.md)** - как внести вклад в проект
- **[Deployment Guide](DEPLOYMENT.md)** - production развертывание на VPS
- **[Security Guide](SECURITY.md)** - меры безопасности
- **[Roadmap](ROADMAP.md)** - планы развития

## 🚀 Планы развития

**v0.3.0 (Q1 2025):**
- 🏷️ Категории и теги для задач
- 🔔 Уведомления через Telegram Bot
- 📊 Расширенная аналитика

**v0.4.0 (Q2 2025):**
- 📝 Подзадачи (subtasks)
- 🔁 Повторяющиеся задачи
- 📱 PWA функциональность

Полный roadmap: [ROADMAP.md](ROADMAP.md)

## 🤝 Вклад в проект

Мы приветствуем контрибьюции! Пожалуйста, прочитайте [CONTRIBUTING.md](CONTRIBUTING.md) для деталей.

### Quick Start для контрибьюторов

1. Fork репозитория
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'feat: добавлена классная фича'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

**Code Style:**
- Backend: PEP 8, black formatter, type hints
- Frontend: ESLint, Prettier
- Commits: [Conventional Commits](https://www.conventionalcommits.org/)

## 🔒 Безопасность

- ✅ HTTPS обязателен для production
- ✅ Telegram initData HMAC-SHA256 validation
- ✅ CORS настроен через environment variables
- ✅ SQL injection защита (SQLAlchemy ORM)
- ✅ Rate limiting (можно добавить slowapi)
- ✅ Environment secrets (не храним в git)

Для production deployment см. [DEPLOYMENT.md](DEPLOYMENT.md)

## 📜 Лицензия

MIT License - см. [LICENSE](LICENSE) для деталей

## 💬 Поддержка

- **Issues:** [GitHub Issues](https://github.com/nelepuy/vectora/issues)
- **Discussions:** [GitHub Discussions](https://github.com/nelepuy/vectora/discussions)

---

