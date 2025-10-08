# Contributing to Vectora

Спасибо за интерес к проекту Vectora! Мы рады вашему вкладу.

## 📋 Содержание

- [Начало работы](#начало-работы)
- [Процесс разработки](#процесс-разработки)
- [Стандарты кода](#стандарты-кода)
- [Тестирование](#тестирование)
- [Pull Request процесс](#pull-request-процесс)
- [CI/CD](#cicd)

## 🚀 Начало работы

### Требования

- Python 3.11+
- Node.js 18+
- Docker и Docker Compose
- Git

### Настройка окружения

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/yourusername/Vectora.git
   cd Vectora
   ```

2. **Backend setup:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   ```

3. **Frontend setup:**
   ```bash
   cd frontend
   npm install
   ```

4. **Запустите в Docker:**
   ```bash
   docker-compose up -d
   ```

## 🔄 Процесс разработки

### Ветвление

- `main` - стабильная версия, готовая к продакшн
- `develop` - активная разработка
- `feature/feature-name` - новые функции
- `fix/bug-description` - исправления багов
- `hotfix/critical-fix` - критические исправления для продакшн

### Рабочий процесс

1. Создайте новую ветку от `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. Вносите изменения с понятными коммитами:
   ```bash
   git add .
   git commit -m "feat: добавлен компонент статистики задач"
   ```

3. Регулярно синхронизируйтесь с `develop`:
   ```bash
   git fetch origin
   git rebase origin/develop
   ```

4. Пушьте изменения и создавайте Pull Request:
   ```bash
   git push origin feature/your-feature-name
   ```

### Формат коммитов

Следуйте [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - новая функциональность
- `fix:` - исправление бага
- `docs:` - изменения в документации
- `style:` - форматирование, точки с запятой и т.д.
- `refactor:` - рефакторинг кода
- `test:` - добавление тестов
- `chore:` - обновление зависимостей, конфигурации

**Примеры:**
```
feat: добавлена фильтрация задач по приоритету
fix: исправлена ошибка сохранения даты в календаре
docs: обновлена документация API
test: добавлены тесты для модуля аутентификации
```

## 📝 Стандарты кода

### Backend (Python)

- **Стиль:** PEP 8
- **Линтер:** flake8, black
- **Типизация:** type hints для всех функций
- **Документация:** docstrings в Google style

```python
def create_task(
    db: Session,
    task: schemas.TaskCreate,
    user_id: str
) -> models.Task:
    """
    Создает новую задачу в базе данных.
    
    Args:
        db: Сессия базы данных
        task: Данные новой задачи
        user_id: ID пользователя Telegram
        
    Returns:
        Созданная задача
        
    Raises:
        ValidationError: Если данные задачи некорректны
    """
    # implementation
```

- **Запустите форматирование:**
  ```bash
  cd backend
  black app/
  flake8 app/
  ```

### Frontend (React)

- **Стиль:** ESLint + Prettier
- **Компоненты:** Функциональные компоненты с хуками
- **Именование:** PascalCase для компонентов, camelCase для функций

```jsx
// Хороший пример
const TaskFilters = ({ onFilterChange, filters }) => {
  const [searchTerm, setSearchTerm] = useState('');
  
  useEffect(() => {
    const timer = setTimeout(() => {
      onFilterChange({ ...filters, search: searchTerm });
    }, 300);
    
    return () => clearTimeout(timer);
  }, [searchTerm]);
  
  return (
    <div className="task-filters">
      {/* JSX */}
    </div>
  );
};
```

- **Запустите проверку:**
  ```bash
  cd frontend
  npm run lint
  npm run format
  ```

## 🧪 Тестирование

### Backend тесты

```bash
cd backend
pytest tests/ -v --cov=app
```

**Обязательные тесты:**
- Unit тесты для CRUD операций
- Integration тесты для API endpoints
- Тесты аутентификации
- Минимальное покрытие: 80%

### Frontend тесты

```bash
cd frontend
npm test
npm run test:coverage
```

**Типы тестов:**
- Component tests (React Testing Library)
- Integration tests для hooks
- E2E tests (Cypress/Playwright) для критичных флоу

### Перед коммитом

```bash
# Backend
cd backend
pytest tests/ -v
black app/ --check
flake8 app/

# Frontend
cd frontend
npm test
npm run lint
npm run build
```

## 🔀 Pull Request процесс

### Чеклист перед созданием PR

- [ ] Код соответствует стандартам проекта
- [ ] Все тесты проходят
- [ ] Добавлены новые тесты для новой функциональности
- [ ] Документация обновлена (README, API.md)
- [ ] Нет конфликтов с `develop` веткой
- [ ] Коммиты имеют понятные сообщения
- [ ] .env.example обновлен (если добавлены новые переменные)

### Создание Pull Request

1. **Заголовок:** Краткое описание изменений
   ```
   feat: Добавлена система фильтрации и поиска задач
   ```

2. **Описание:** Используйте шаблон
   ```markdown
   ## Описание
   Добавлена возможность фильтрации задач по статусу, приоритету и поиску по тексту.
   
   ## Изменения
   - ✨ Новый компонент TaskFilters
   - 🔧 Расширен API endpoint GET /tasks с query параметрами
   - ✅ Добавлены тесты для фильтрации
   
   ## Тестирование
   - [ ] Backend тесты проходят
   - [ ] Frontend билдится без ошибок
   - [ ] Ручное тестирование выполнено
   
   ## Скриншоты
   [Если применимо]
   
   ## Связанные Issue
   Closes #123
   ```

3. **Ревью:** Дождитесь ревью от мейнтейнеров

### Code Review Guidelines

**Для авторов:**
- Отвечайте на комментарии конструктивно
- Вносите запрошенные изменения
- Обновляйте PR при изменениях в `develop`

**Для ревьюеров:**
- Проверьте соответствие стандартам
- Запустите код локально
- Оставляйте конструктивные комментарии
- Одобряйте через GitHub Review

## 🤖 CI/CD

### Автоматические проверки

При каждом push и PR автоматически запускаются:

1. **Backend Tests** (`.github/workflows/backend-tests.yml`)
   - Установка зависимостей
   - Запуск pytest с покрытием
   - PostgreSQL сервис для интеграционных тестов
   - Загрузка coverage в Codecov

2. **Frontend Lint & Build** (`.github/workflows/frontend-lint.yml`)
   - ESLint проверка
   - Production build
   - Сохранение артефактов

3. **Docker Build** (`.github/workflows/docker-build.yml`)
   - Сборка backend/frontend образов
   - Проверка docker-compose конфигурации
   - Health check для API

### Статусы проверок

PR может быть смержен только если:
- ✅ Все тесты проходят
- ✅ Build успешен
- ✅ Нет конфликтов
- ✅ Получен approve от мейнтейнера

### Локальный запуск CI проверок

```bash
# Backend тесты (как в CI)
cd backend
pytest tests/ -v --cov=app --cov-report=xml

# Frontend build (как в CI)
cd frontend
npm ci
npm run lint
npm run build

# Docker build (как в CI)
docker-compose config
docker-compose up -d
curl http://localhost:8000/docs
docker-compose down
```

## 📚 Дополнительные ресурсы

- [Документация API](backend/API.md)
- [Backend README](backend/README.md)
- [Frontend README](frontend/README.md)
- [Telegram Bot API](https://core.telegram.org/bots/webapps)

## 💬 Вопросы и поддержка

- **Issues:** Создавайте issue для багов и предложений
- **Discussions:** Используйте GitHub Discussions для вопросов
- **Telegram:** [Ссылка на группу поддержки]

## 📜 Лицензия

Убедитесь, что ваш вклад соответствует лицензии проекта (см. [LICENSE](LICENSE)).

---

Спасибо за вклад в Vectora! 🚀
