# Vectora Backend# Vectora Backend (FastAPI)



FastAPI backend for Vectora task management system.Бэкенд для Telegram Mini App на FastAPI + SQLAlchemy + PostgreSQL с поддержкой аутентификации через Telegram WebApp.



## Features## ✨ Возможности



- RESTful API for task management- ✅ **CRUD API для задач** с поддержкой фильтрации и поиска

- Telegram WebApp authentication- ✅ **Telegram аутентификация** через initData

- PostgreSQL database with SQLAlchemy ORM- ✅ **Автодокументация** Swagger UI (`/docs`) и ReDoc (`/redoc`)

- Alembic migrations- ✅ **Пагинация и фильтрация** задач

- CORS support- ✅ **Структурированное логирование**

- ✅ **Централизованная обработка ошибок**

## Setup- ✅ **Unit и интеграционные тесты**

- ✅ **Настраиваемый CORS**

```bash

python -m venv venv## 🚀 Быстрый старт

source venv/bin/activate

pip install -r requirements.txt### Локальная разработка

```

```powershell

## Configurationcd backend

python -m venv venv

Create `.env` file:.\venv\Scripts\activate

```pip install -r requirements.txt

DATABASE_URL=postgresql://user:password@host:5432/dbnameuvicorn app.main:app --reload --port 8000

SECRET_KEY=your-secret-key-here```

TELEGRAM_BOT_TOKEN=your-bot-token

DEBUG=falseAPI будет доступно на http://localhost:8000

BACKEND_CORS_ORIGINS=https://nelepuy.github.io

```### Docker



## Database Migrations```powershell

docker-compose up -d backend

```bash```

# Apply migrations

alembic upgrade head## 📁 Структура проекта



# Create new migration```

alembic revision --autogenerate -m "description"backend/

```├── app/

│   ├── routers/          # API endpoints

## Run Development Server│   │   └── tasks.py      # CRUD операции с задачами

│   ├── auth.py           # Telegram аутентификация

```bash│   ├── crud.py           # Операции с БД

uvicorn app.main:app --reload│   ├── database.py       # Подключение к PostgreSQL

```│   ├── exceptions.py     # Кастомные исключения

│   ├── logging_config.py # Настройка логирования

## API Endpoints│   ├── main.py           # FastAPI приложение

│   ├── models.py         # SQLAlchemy модели

- `GET /health` - Health check│   ├── schemas.py        # Pydantic схемы

- `GET /version` - API version│   └── settings.py       # Конфигурация

- `GET /tasks/` - List tasks├── migrations/           # Alembic миграции

- `POST /tasks/` - Create task├── tests/               # Тесты

- `PUT /tasks/{id}` - Update task│   ├── conftest.py      # Pytest fixtures

- `DELETE /tasks/{id}` - Delete task│   ├── test_api.py      # API тесты

│   ├── test_auth.py     # Тесты аутентификации

## Deployment│   └── test_crud.py     # CRUD тесты

├── requirements.txt     # Зависимости

Railway deployment uses root `Dockerfile` which copies from `backend/` directory.├── pytest.ini          # Конфигурация pytest

└── API.md              # Документация API

Environment variables are set in Railway dashboard.```


## ⚙️ Переменные окружения

Создайте `app/.env` на основе `.env.example`:

```env
# Режим разработки
DEBUG=true

# База данных
DATABASE_URL=postgresql://postgres:postgres@db:5432/tasks

# CORS (разделённые запятыми домены)
BACKEND_CORS_ORIGINS=http://localhost:3000,https://your-app.com

# Telegram Bot Token (обязательно для продакшена)
TELEGRAM_BOT_TOKEN=your-telegram-bot-token-here
```

## 🧪 Тестирование

### Запуск всех тестов

```powershell
# Windows
.\run_tests.ps1

# Linux/Mac
./run_tests.sh
```

### Запуск конкретных тестов

```powershell
pytest tests/test_api.py -v
pytest tests/test_crud.py::test_create_task -v
```

### Тесты с покрытием

```powershell
pytest --cov=app --cov-report=html
```

Отчёт будет в `htmlcov/index.html`

## 📊 API Endpoints

### Основные

- `GET /health` — Healthcheck
- `GET /version` — Версия API
- `GET /docs` — Swagger UI
- `GET /redoc` — ReDoc документация

### Задачи

- `GET /tasks/` — Список задач с фильтрацией
- `GET /tasks/{id}` — Получить задачу
- `POST /tasks/` — Создать задачу
- `PUT /tasks/{id}` — Обновить задачу
- `DELETE /tasks/{id}` — Удалить задачу

**Параметры фильтрации:**
- `skip`, `limit` — пагинация
- `status` — фильтр по статусу (true/false)
- `priority` — фильтр по приоритету (low/normal/high)
- `search` — поиск по названию и описанию

Подробная документация в [API.md](API.md)

## 🔐 Аутентификация

API использует Telegram WebApp initData для аутентификации.

**Заголовок запроса:**
```
X-Telegram-Init-Data: <initData из window.Telegram.WebApp>
```

В режиме `DEBUG=true` аутентификация не требуется (используется test_user).

## 🗄️ Миграции базы данных

```powershell
# Применить миграции
alembic upgrade head

# Создать новую миграцию
alembic revision --autogenerate -m "описание изменений"

# Откатить последнюю миграцию
alembic downgrade -1
```

## 📝 Логирование

Логи выводятся в stdout в формате:
```
2025-10-07 10:00:00 - vectora - INFO - Запрос: GET /tasks/
```

Уровень логирования зависит от `DEBUG`:
- `DEBUG=true` → уровень DEBUG
- `DEBUG=false` → уровень INFO

## 🚀 Деплой

### Продакшен чеклист

1. ✅ Установите `DEBUG=false`
2. ✅ Укажите реальный `TELEGRAM_BOT_TOKEN`
3. ✅ Настройте `BACKEND_CORS_ORIGINS` на ваши домены
4. ✅ Используйте надёжный `DATABASE_URL` (не localhost)
5. ✅ Запускайте за HTTPS (Nginx/Traefik)
6. ✅ Настройте мониторинг и алерты

### Docker production

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Разработка

### Добавление новых endpoint'ов

1. Создайте router в `app/routers/`
2. Добавьте CRUD функции в `app/crud.py`
3. Определите Pydantic схемы в `app/schemas.py`
4. Подключите router в `app/main.py`
5. Напишите тесты в `tests/`

### Code style

- Следуйте PEP 8
- Используйте type hints
- Документируйте функции docstring'ами
- Пишите тесты для новой функциональности

## 📚 Дополнительная информация

- [API документация](API.md)
- [Alembic миграции](migrations/)
- [Примеры тестов](tests/)