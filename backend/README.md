# Vectora Backend (FastAPI)

Бэкенд для Telegram Mini App на FastAPI + SQLAlchemy + PostgreSQL с поддержкой аутентификации через Telegram WebApp.

## ✨ Возможности

- ✅ **CRUD API для задач** с поддержкой фильтрации и поиска
- ✅ **Telegram аутентификация** через initData
- ✅ **Автодокументация** Swagger UI (`/docs`) и ReDoc (`/redoc`)
- ✅ **Пагинация и фильтрация** задач
- ✅ **Структурированное логирование**
- ✅ **Централизованная обработка ошибок**
- ✅ **Unit и интеграционные тесты**
- ✅ **Настраиваемый CORS**

## 🚀 Быстрый старт

### Локальная разработка

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API будет доступно на http://localhost:8000

### Docker

```powershell
docker-compose up -d backend
```

## 📁 Структура проекта

```
backend/
├── app/
│   ├── routers/          # API endpoints
│   │   └── tasks.py      # CRUD операции с задачами
│   ├── auth.py           # Telegram аутентификация
│   ├── crud.py           # Операции с БД
│   ├── database.py       # Подключение к PostgreSQL
│   ├── exceptions.py     # Кастомные исключения
│   ├── logging_config.py # Настройка логирования
│   ├── main.py           # FastAPI приложение
│   ├── models.py         # SQLAlchemy модели
│   ├── schemas.py        # Pydantic схемы
│   └── settings.py       # Конфигурация
├── migrations/           # Alembic миграции
├── tests/               # Тесты
│   ├── conftest.py      # Pytest fixtures
│   ├── test_api.py      # API тесты
│   ├── test_auth.py     # Тесты аутентификации
│   └── test_crud.py     # CRUD тесты
├── requirements.txt     # Зависимости
├── pytest.ini          # Конфигурация pytest
└── API.md              # Документация API
```

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