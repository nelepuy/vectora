# 🚀 Railway Deployment Guide

## ✅ Ветки созданы!

Созданы отдельные ветки для Railway деплоя:

- **`railway-backend`** — Backend (FastAPI + PostgreSQL)
- **`railway-bot`** — Telegram Bot (Aiogram)
- **`main`** — Полный проект (для разработки)

---

## 📋 Деплой на Railway

### 1. Backend (FastAPI)

1. Откройте https://railway.app/dashboard
2. **New Project** → **Deploy from GitHub repo**
3. Выберите репозиторий: `nelepuy/vectora`
4. **Выберите ветку:** `railway-backend` ⚠️
5. Railway автоматически определит Python проект

**Добавьте переменные окружения (Variables):**

```env
SECRET_KEY=<сгенерируйте случайный ключ>
TELEGRAM_BOT_TOKEN=8314825408:AAESxb1LnlIIn_N5JaeGt2XBctqzD_eSVrQ
ALLOWED_ORIGINS=https://nelepuy.github.io
PORT=8000
```

**Добавьте PostgreSQL:**
- **New** → **Database** → **PostgreSQL**
- Railway автоматически добавит переменную `DATABASE_URL`

**Start Command (если нужно):**
```bash
alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

### 2. Bot (Aiogram)

1. **New Service** → **GitHub Repo** → `nelepuy/vectora`
2. **Выберите ветку:** `railway-bot` ⚠️
3. Railway автоматически определит Python проект

**Добавьте переменные окружения:**

```env
BOT_TOKEN=8314825408:AAESxb1LnlIIn_N5JaeGt2XBctqzD_eSVrQ
WEBAPP_URL=https://nelepuy.github.io/vectora
API_URL=<ваш backend URL из Railway>
```

**Start Command (если нужно):**
```bash
python bot.py
```

---

### 3. Frontend (GitHub Pages) — БЕСПЛАТНО!

Не деплойте на Railway, используйте GitHub Pages:

```powershell
cd frontend

# 1. Установите gh-pages
npm install gh-pages --save-dev

# 2. Добавьте в package.json:
# "homepage": "https://nelepuy.github.io/vectora"
# "scripts": {
#   "predeploy": "npm run build",
#   "deploy": "gh-pages -d build"
# }

# 3. Создайте .env.production с Backend URL из Railway
$backendUrl = "https://your-backend.up.railway.app"
"REACT_APP_API_URL=$backendUrl" | Out-File .env.production

# 4. Деплой
npm run deploy
```

**Активируйте GitHub Pages:**
1. https://github.com/nelepuy/vectora/settings/pages
2. Source: **Deploy from a branch**
3. Branch: **gh-pages** → **/root**
4. Save

---

## 🔗 После деплоя:

### Обновите переменные окружения:

**Backend:**
- `ALLOWED_ORIGINS=https://nelepuy.github.io`

**Bot:**
- `WEBAPP_URL=https://nelepuy.github.io/vectora`
- `API_URL=https://your-backend.up.railway.app` (получите из Railway)

**Frontend (.env.production):**
- `REACT_APP_API_URL=https://your-backend.up.railway.app`

---

## 🤖 Настройка Menu Button в Telegram

После деплоя frontend на GitHub Pages:

1. Откройте @BotFather
2. `/mybots` → **PlanerSeptember**
3. **Bot Settings** → **Menu Button**
4. **Название:** `Открыть Vectora`
5. **URL:** `https://nelepuy.github.io/vectora`

---

## 💰 Стоимость:

- **Backend (Railway):** ~$3/мес
- **Bot (Railway):** ~$2/мес
- **PostgreSQL (Railway):** Включено
- **Frontend (GitHub Pages):** **БЕСПЛАТНО** ✅

**Итого:** ~$5/мес (покрывается GitHub Student Pack!)

---

## 🔄 Обновление после деплоя:

### Backend:
```bash
git checkout railway-backend
# Сделайте изменения в backend/
git add .
git commit -m "Update backend"
git push
```
Railway автоматически задеплоит!

### Bot:
```bash
git checkout railway-bot
# Сделайте изменения в bot/
git add .
git commit -m "Update bot"
git push
```
Railway автоматически задеплоит!

### Frontend:
```bash
cd frontend
npm run deploy
```

---

## 📊 URLs после деплоя:

- **Frontend:** https://nelepuy.github.io/vectora
- **Backend:** https://vectora-backend-production.up.railway.app (получите из Railway)
- **Bot:** Работает в фоне (логи в Railway)
- **API Docs:** https://your-backend.up.railway.app/docs

---

## 🆘 Troubleshooting:

### Railway не видит ветку?
- Обновите страницу Railway
- Или выберите вручную: Settings → Source → Branch

### Backend не запускается?
- Проверьте логи в Railway
- Убедитесь что DATABASE_URL настроена
- Проверьте что PostgreSQL добавлена

### Bot не отвечает?
- Проверьте логи в Railway
- Убедитесь что BOT_TOKEN правильный
- Проверьте что WEBAPP_URL и API_URL настроены

---

## ✅ Готово!

Теперь у вас:
- ✅ Backend на Railway
- ✅ Bot на Railway
- ✅ Frontend на GitHub Pages
- ✅ Автоматический деплой при `git push`

**Откройте @PlanerPlanerbot в Telegram и протестируйте!** 🎉
