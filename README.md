# 📋 Vectora — Планировщик задач (Telegram Mini App)

[![CI/CD](https://github.com/nelepuy/vectora/actions/workflows/backend-tests.yml/badge.svg)](https://github.com/nelepuy/vectora/actions)
[![Coverage](https://img.shields.io/badge/coverage-85%2B-brightgreen.svg)](./backend/README.md)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/react-18-blue.svg)](https://reactjs.org/)

**Современный task-менеджер** в виде Telegram Mini App с полнофункциональным REST API, интеграцией с Telegram Bot и production-ready архитектурой.

## ✨ Возможности

### Основные
- 📝 **CRUD операции** для задач с полной валидацией
- 🔍 **Фильтрация и поиск** по статусу, приоритету, тексту (debounced)
- 📅 **Календарное представление** (React Big Calendar)
- 📊 **Dashboard со статистикой**: completion rate, приоритеты, overdue задачи
- 🎨 **Тёмная/светлая тема** с синхронизацией Telegram theme
- 📱 **Адаптивный дизайн** для всех устройств

### Технические
- 🔐 **Telegram WebApp Authentication** (HMAC-SHA256 validation)
- ✅ **Comprehensive Testing** (pytest, 85%+ coverage, unit + integration)
- 📝 **Structured Logging** с request/response tracking
- 🚀 **CI/CD Pipeline** (GitHub Actions: тесты, lint, build)
- 🐳 **Docker контейнеризация** (production-ready compose)
- 📚 **API Documentation** (OpenAPI/Swagger, Postman collection)

## 🏗️ Архитектура

**Backend:** FastAPI, SQLAlchemy, Alembic, PostgreSQL  
**Frontend:** React 18, Custom hooks, CSS animations  
**Bot:** Aiogram (WebApp button)  
**Testing:** pytest, pytest-cov, httpx TestClient  
**CI/CD:** GitHub Actions, Docker, Nginx

## 📁 Структура проекта

```
Vectora/
├─ backend/              # FastAPI REST API
│  ├─ app/
│  │  ├─ main.py         # Application entry point с middleware
│  │  ├─ auth.py         # Telegram WebApp authentication
│  │  ├─ crud.py         # Database operations с filtering
│  │  ├─ models.py       # SQLAlchemy models
│  │  ├─ schemas.py      # Pydantic schemas (v2)
│  │  ├─ exceptions.py   # Centralized error handling
│  │  └─ routers/        # API endpoints
│  ├─ tests/             # pytest test suite (85%+ coverage)
│  ├─ migrations/        # Alembic database migrations
│  └─ API.md             # Comprehensive API documentation
│
├─ frontend/             # React SPA
│  ├─ src/
│  │  ├─ components/
│  │  │  ├─ TaskList.jsx     # Task management
│  │  │  ├─ TaskFilters.jsx  # Search & filtering (debounced)
│  │  │  ├─ TaskStats.jsx    # Dashboard statistics
│  │  │  └─ CalendarView.jsx # Calendar interface
│  │  └─ hooks/
│  │     └─ useTelegramWebApp.js
│  └─ Dockerfile
│
├─ bot/                  # Telegram Bot (aiogram)
│  └─ bot.py             # WebApp button handler
│
├─ .github/
│  ├─ workflows/         # CI/CD pipelines
│  │  ├─ backend-tests.yml
│  │  ├─ frontend-lint.yml
│  │  └─ docker-build.yml
│  ├─ ISSUE_TEMPLATE/    # Bug & feature templates
│  └─ PULL_REQUEST_TEMPLATE.md
│
├─ CONTRIBUTING.md       # Contribution guidelines
├─ DEPLOYMENT.md         # Production deployment guide
├─ ROADMAP.md            # Development roadmap 2025
└─ docker-compose.yml    # Local development setup
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

- **[API Documentation](backend/API.md)** - подробное описание всех endpoints
- **[Contributing Guide](CONTRIBUTING.md)** - как внести вклад в проект
- **[Development Roadmap](ROADMAP.md)** - планы развития на 2025 год
- **[Deployment Guide](DEPLOYMENT.md)** - production deployment пошагово

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

**Сделано с ❤️ для Telegram сообщества**