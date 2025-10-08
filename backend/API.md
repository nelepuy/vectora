# API Документация

## Обзор

Vectora API предоставляет RESTful интерфейс для управления задачами в Telegram Mini App.

Базовый URL: `http://localhost:8000` (разработка) или ваш продакшен домен.

## Аутентификация

API использует Telegram WebApp initData для аутентификации пользователей.

**Заголовок:**
```
X-Telegram-Init-Data: <initData из Telegram.WebApp>
```

В режиме разработки (DEBUG=true) аутентификация необязательна — используется test_user.

## Endpoints

### Healthcheck

```http
GET /health
```

Проверка доступности сервиса.

**Ответ:**
```json
{
  "status": "ok"
}
```

---

### Получить список задач

```http
GET /tasks/
```

**Query параметры:**
- `skip` (int, default=0): Пропустить N записей
- `limit` (int, default=100): Максимум записей (1-500)
- `status` (bool, optional): Фильтр по статусу (true=выполнено)
- `priority` (string, optional): Фильтр по приоритету (low/normal/high)
- `search` (string, optional): Поиск по названию и описанию

**Примеры:**
```bash
# Все задачи
GET /tasks/

# Только активные высокого приоритета
GET /tasks/?status=false&priority=high

# Поиск
GET /tasks/?search=важная

# Пагинация
GET /tasks/?skip=10&limit=20
```

**Ответ:**
```json
[
  {
    "id": 1,
    "user_id": "123456",
    "title": "Важная задача",
    "description": "Описание задачи",
    "date_time": "2025-10-07T10:00:00",
    "priority": "high",
    "status": false,
    "position": 0,
    "created_at": "2025-10-07T09:00:00"
  }
]
```

---

### Получить задачу по ID

```http
GET /tasks/{task_id}
```

**Ответ:** Объект задачи или 404 если не найдена.

---

### Создать задачу

```http
POST /tasks/
```

**Body:**
```json
{
  "title": "Название задачи",
  "description": "Описание (опционально)",
  "date_time": "2025-10-07T15:00:00",
  "priority": "normal",
  "position": 0
}
```

**Ответ:** Созданная задача со статусом 201.

---

### Обновить задачу

```http
PUT /tasks/{task_id}
```

**Body (все поля опциональны):**
```json
{
  "title": "Новое название",
  "status": true,
  "priority": "high"
}
```

**Ответ:** Обновлённая задача.

---

### Удалить задачу

```http
DELETE /tasks/{task_id}
```

**Ответ:** 204 No Content

---

## Коды ошибок

- `400` — Bad Request (некорректные данные)
- `401` — Unauthorized (нет авторизации)
- `404` — Not Found (задача не найдена)
- `422` — Unprocessable Entity (ошибка валидации)
- `500` — Internal Server Error

## Модели данных

### Task

```typescript
{
  id: number;              // Уникальный ID
  user_id: string;         // ID пользователя Telegram
  title: string;           // Название (обязательно)
  description?: string;    // Описание
  date_time?: string;      // Дата и время (ISO 8601)
  priority: "low" | "normal" | "high";  // Приоритет
  status: boolean;         // Статус выполнения
  position: number;        // Позиция для сортировки
  created_at: string;      // Дата создания
}
```

## Интерактивная документация

- Swagger UI: `/docs`
- ReDoc: `/redoc`
