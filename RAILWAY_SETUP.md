# Деплой на Railway

## Проблема которую вы видели:
**"Error creating build plan with Railpack"** — Railway не понял структуру проекта.

## Решение:

У вас **monorepo** (несколько приложений в одном репозитории). Railway нужно указать какое приложение деплоить.

### Шаг 1: Создайте 3 отдельных сервиса в Railway

1. Откройте https://railway.app/dashboard
2. Создайте **New Project** → **Deploy from GitHub repo**
3. Выберите репозиторий `nelepuy/vectora`

### Шаг 2: Настройте каждый сервис

#### Сервис 1: Backend

**Settings → Root Directory:**
```
backend
```

**Settings → Build Command:**
```bash
pip install -r requirements.txt
```

**Settings → Start Command:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Variables (переменные окружения):**
```
DATABASE_URL=${{Postgres.DATABASE_URL}}
SECRET_KEY=your-generated-secret-key
TELEGRAM_BOT_TOKEN=8314825408:AAHbl_06QBEG8B64FiP8Cb0YfwoaV-7H2lQ
ALLOWED_ORIGINS=https://your-frontend-url.up.railway.app
```

---

#### Сервис 2: Bot

**Settings → Root Directory:**
```
bot
```

**Settings → Start Command:**
```bash
python bot.py
```

**Variables:**
```
BOT_TOKEN=8314825408:AAHbl_06QBEG8B64FiP8Cb0YfwoaV-7H2lQ
WEBAPP_URL=https://your-frontend-url.up.railway.app
API_URL=https://your-backend-url.up.railway.app
```

---

#### Сервис 3: Frontend (или лучше GitHub Pages)

**Вариант A: Railway**
- Root Directory: `frontend`
- Build: автоматически определится (npm)

**Вариант B: GitHub Pages (рекомендуется, бесплатно!)**

```bash
cd frontend

# 1. Добавьте в package.json:
"homepage": "https://nelepuy.github.io/vectora"

# 2. Установите gh-pages
npm install --save-dev gh-pages

# 3. Добавьте скрипты в package.json:
"scripts": {
  "predeploy": "npm run build",
  "deploy": "gh-pages -d build"
}

# 4. Создайте .env.production с URL backend из Railway
echo "REACT_APP_API_URL=https://your-backend.up.railway.app" > .env.production

# 5. Деплой
npm run deploy
```

---

### Шаг 3: Добавьте PostgreSQL

1. В Railway dashboard → **New** → **Database** → **PostgreSQL**
2. Railway автоматически создаст переменную `DATABASE_URL`
3. Она будет доступна в backend через `${{Postgres.DATABASE_URL}}`

---

### Шаг 4: Примените миграции

После деплоя backend:

```bash
# В Railway dashboard → Backend → Settings → Deploy
# Добавьте в "Deploy Command":
alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## Быстрая альтернатива: Используйте один сервис

Если не хотите настраивать 3 сервиса отдельно:

### Вариант: Railway backend + Railway bot + GitHub Pages frontend

1. **Backend на Railway:**
   - Root Directory: `backend`
   - Добавьте PostgreSQL
   - Получите URL (например: `https://vectora-backend.up.railway.app`)

2. **Bot на Railway:**
   - Root Directory: `bot`
   - Укажите URL frontend и backend в переменных

3. **Frontend на GitHub Pages (БЕСПЛАТНО):**
   ```bash
   cd frontend
   npm install gh-pages --save-dev
   npm run deploy
   ```

---

## Стоимость:

- **Backend:** ~$3/мес
- **Bot:** ~$2/мес  
- **PostgreSQL:** Включено
- **Frontend (GitHub Pages):** БЕСПЛАТНО

**Итого:** ~$5/мес (покрывается GitHub Student Pack!)

---

## Что делать СЕЙЧАС:

1. **Закоммитьте новые файлы:**
   ```bash
   git add backend/railway.json bot/railway.json frontend/railway.json
   git commit -m "Add Railway configuration"
   git push
   ```

2. **Попробуйте снова деплой в Railway:**
   - Откройте проект в Railway
   - Нажмите **Deploy**
   - Теперь Railway должен понять структуру

3. **Или настройте через UI** (как описано выше)

---

Хотите чтобы я помог настроить через UI или предпочитаете автоматический способ?
