# 🌐 Варианты деплоя Vectora (работают в России)

Все варианты протестированы и **доступны из России** в 2025 году.

---

## 🎓 GitHub Student Pack — Рекомендованные варианты

### ✅ 1. **DigitalOcean** (⭐ Лучший вариант!)

**Что даёт GitHub Student Pack:**
- $200 кредитов на 1 год
- Droplets (виртуальные серверы)
- Managed PostgreSQL
- App Platform (PaaS, как Heroku)

**Почему DigitalOcean:**
- ✅ Работает в России без VPN
- ✅ Простая настройка
- ✅ Русскоязычная документация
- ✅ Дешёвый (~$12/месяц с запасом)
- ✅ Автоматический HTTPS через Let's Encrypt

**Быстрый деплой:**
```bash
# 1. Получите $200 через GitHub Student Pack
# https://education.github.com/pack

# 2. Создайте аккаунт на DigitalOcean
# https://www.digitalocean.com/

# 3. Установите doctl
winget install DigitalOcean.Doctl

# 4. Авторизуйтесь
doctl auth init

# 5. Запустите наш скрипт автодеплоя
.\deploy-digitalocean.ps1
```

**Стоимость с GitHub Student Pack:**
- 1 год: $0 (бесплатно, кредиты $200)
- Потом: ~$12/месяц

---

### ✅ 2. **Heroku** (через Student Pack)

**Что даёт GitHub Student Pack:**
- $13/месяц кредитов на 2 года ($312 всего)
- Heroku Eco Dynos
- Heroku Postgres

**Почему Heroku:**
- ✅ Работает в России
- ✅ Самый простой деплой (git push)
- ✅ Автоматический HTTPS
- ✅ Бесплатная PostgreSQL (Hobby Dev)

**Быстрый деплой:**
```bash
# 1. Получите Heroku через GitHub Student Pack
# https://education.github.com/pack

# 2. Установите Heroku CLI
winget install Heroku.HerokuCLI

# 3. Авторизуйтесь
heroku login

# 4. Запустите наш скрипт
.\deploy-heroku.ps1
```

**Стоимость:**
- С Student Pack: $13/месяц кредитов (покрывает всё)
- Eco Dynos: $5/месяц за приложение
- PostgreSQL Hobby Dev: бесплатно

---

### ✅ 3. **Railway** (🔥 Новинка 2024)

**Что даёт GitHub Student Pack:**
- $100 кредитов + $5/месяц на 1 год

**Почему Railway:**
- ✅ Работает в России
- ✅ Самый современный интерфейс
- ✅ Автоматический деплой из GitHub
- ✅ Встроенная PostgreSQL
- ✅ Бесплатный HTTPS

**Быстрый деплой:**
```bash
# 1. Получите Railway через GitHub Student Pack
# https://education.github.com/pack

# 2. Установите Railway CLI
npm install -g @railway/cli

# 3. Авторизуйтесь
railway login

# 4. Запустите наш скрипт
.\deploy-railway.ps1
```

**Стоимость:**
- С Student Pack: $5/месяц (покрывает всё)
- После: ~$10/месяц

---

### ✅ 4. **Namecheap** (для VPS)

**Что даёт GitHub Student Pack:**
- 1 год бесплатного SSL сертификата
- Скидки на домены

**Для VPS деплоя:**
- VPS от Aeza.net (~300₽/месяц, работает в России)
- VDS.ru (~500₽/месяц, российский хостинг)
- Timeweb (~350₽/месяц, работает в России)

---

## 🚀 Рекомендация для вас

### Вариант 1: **DigitalOcean App Platform** (⭐ Рекомендую!)

**Преимущества:**
- 🎓 $200 бесплатно через Student Pack (1 год)
- ☁️ Полностью управляемый PaaS
- 🔒 Автоматический HTTPS
- 📊 Встроенный мониторинг
- 🐳 Поддержка Docker
- 🌍 Работает в России

**Запуск за 5 минут:**
```powershell
# Запустите готовый скрипт
.\deploy-digitalocean.ps1
```

---

### Вариант 2: **Railway** (для самого быстрого старта)

**Преимущества:**
- 🚄 Деплой за 2 минуты
- 🎨 Красивый интерфейс
- 🔄 Автодеплой из GitHub
- 💳 $100 кредитов через Student Pack

**Запуск за 2 минуты:**
```powershell
.\deploy-railway.ps1
```

---

### Вариант 3: **Локально + localtunnel** (бесплатно навсегда)

**Если не хочется платить:**
```powershell
.\start.ps1
```

Работает через локальный туннель, подходит для разработки и демо.

---

## 📋 Сравнение

| Платформа | Стоимость с Student Pack | HTTPS | Доступность в РФ | Сложность |
|-----------|-------------------------|-------|------------------|-----------|
| **DigitalOcean** | $0 (1 год) | ✅ Авто | ✅ Работает | ⭐⭐ |
| **Railway** | $5/мес | ✅ Авто | ✅ Работает | ⭐ |
| **Heroku** | Покрыто кредитами | ✅ Авто | ✅ Работает | ⭐ |
| **VPS (Aeza)** | 300₽/мес | ⚙️ Настройка | ✅ Работает | ⭐⭐⭐⭐ |
| **localtunnel** | Бесплатно | ✅ Авто | ✅ Работает | ⭐ |

---

## 🎯 Что выбрать?

### Если вы студент с GitHub Student Pack:
1. **DigitalOcean** — лучший баланс цены, функций и стабильности
2. **Railway** — если нужна максимальная скорость деплоя
3. **Heroku** — если хотите классику

### Если хотите бесплатно:
1. **localtunnel** (локально) — `.\start.ps1`
2. **Railway** (free tier) — 500 часов/месяц бесплатно

### Если нужна полная стабильность:
1. **VPS** (Aeza.net, VDS.ru, Timeweb) — полный контроль

---

## 📝 Следующие шаги

### Выберите платформу и запустите скрипт:

```powershell
# DigitalOcean (рекомендую)
.\deploy-digitalocean.ps1

# Railway (самый быстрый)
.\deploy-railway.ps1

# Heroku (классика)
.\deploy-heroku.ps1

# Локально (бесплатно)
.\start.ps1
```

---

## 🆘 Поддержка

**Проблемы с доступом?**
- DigitalOcean: работает напрямую из РФ
- Railway: работает напрямую из РФ
- Heroku: работает напрямую из РФ

**Вопросы?**
- Telegram: @PlanerPlanerbot
- GitHub Issues: nelepuy/vectora

---

## 🔗 Полезные ссылки

- [GitHub Student Pack](https://education.github.com/pack)
- [DigitalOcean Student](https://www.digitalocean.com/github-students)
- [Heroku Student](https://www.heroku.com/github-students)
- [Railway Student](https://railway.app/github-student)
- [Aeza.net VPS](https://aeza.net/) (российский хостинг)
- [Timeweb](https://timeweb.com/) (российский хостинг)

---

💡 **Совет:** Начните с **DigitalOcean** — получите $200 через Student Pack и используйте 1 год бесплатно!
