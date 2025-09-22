# Vectora Backend (FastAPI)

Бэкенд сервиса задач на FastAPI + SQLAlchemy + PostgreSQL. Готов к локальному запуску и деплою.
## Возможности

- CRUD по задачам: `/tasks/`
- Pydantic-схемы и автодокументация Swagger (`/docs`)
- Настраиваемый CORS через переменные окружения

## Быстрый старт

```powershell
cd backend
python -m venv venv; .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
API: http://localhost:8000 (Swagger: /docs)

## Переменные окружения (`app/.env`)

```
DATABASE_URL=postgresql://postgres:postgres@db:5432/tasks
JWT_SECRET=change-me
BACKEND_CORS_ORIGINS=https://your-frontend-domain.com
BACKEND_CORS_REGEX=
```
## Структура

```
backend/
└─ app/
  ├─ routers/      # эндпоинты
  # Vectora Backend (FastAPI)

  Небольшой бэкенд на FastAPI + SQLAlchemy + PostgreSQL для задач. Готов к локальному запуску и деплою.

  ## Возможности

  - REST CRUD по маршрутам `/tasks/`
  - Pydantic‑схемы, автоматическая документация Swagger (`/docs`)
  - CORS через переменные окружения (origin‑лист и/или regex)

  ## Запуск локально

  ```powershell
  cd backend
  python -m venv venv; .\venv\Scripts\activate
  pip install -r requirements.txt
  uvicorn app.main:app --reload --port 8000
  ```

  API: http://localhost:8000 (Swagger: /docs)

  ## Окружение (`app/.env`)

  ```
  DATABASE_URL=postgresql://postgres:postgres@db:5432/tasks
  JWT_SECRET=change-me
  BACKEND_CORS_ORIGINS=https://your-frontend-domain.com
  BACKEND_CORS_REGEX=
  ```

  ## Структура

  ```
  backend/
  └─ app/
     ├─ routers/      # эндпоинты
     ├─ models.py     # модели БД
     ├─ schemas.py    # Pydantic‑схемы
     ├─ crud.py       # операции с БД
     ├─ database.py   # подключение к БД
     ├─ settings.py   # конфиг (CORS и др.)
     └─ main.py       # приложение FastAPI
  ```

  ## Миграции (Alembic)

  ```powershell
  alembic upgrade head
  ```

  ## Деплой

  - Задайте CORS через `BACKEND_CORS_ORIGINS` или `BACKEND_CORS_REGEX`
  - Храните `DATABASE_URL`, `JWT_SECRET` в переменных окружения/секретах
  - Рекомендуется запускать под реверс‑прокси (Nginx) с HTTPS