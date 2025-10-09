# 🚀 Быстрый старт Vectora

## Что нужно:
- ✅ Windows с Docker Desktop
- ✅ Node.js (для туннеля)
- ✅ 5-10 минут времени

---

## Шаг 1: Запустите приложение

```powershell
# Токен уже в bot/.env, просто запустите:
.\start.ps1
```

Скрипт автоматически:
- ✅ Запустит Docker контейнеры
- ✅ Применит миграции БД
- ✅ Запустит туннель (localtunnel)
- ✅ Покажет публичный HTTPS URL

**Скопируйте URL** из вывода (вида: `https://...loca.lt`)

---

## Шаг 2: Настройте Menu Button

1. Откройте @BotFather в Telegram
2. Отправьте: `/mybots`
3. Выберите: **PlanerSeptember**
4. Нажмите: **Bot Settings** → **Menu Button**
5. Нажмите: **Configure Menu Button**
6. Введите:
   - **Название:** `Открыть Vectora`
   - **URL:** (вставьте HTTPS URL из скрипта)

---

## Шаг 3: Тестируйте!

1. Найдите бота: @PlanerPlanerbot
2. Отправьте: `/start`
3. Нажмите кнопку: **"🚀 Открыть Vectora"**

**Приложение откроется прямо в Telegram!** 🎉

**Попробуйте:**
- ✅ Создать задачу (➕)
- ✅ Фильтры по категориям
- ✅ Календарь
- ✅ Темы (🌙)
- ✅ Редактирование (двойной клик)

---

## 🐛 Проблемы?

### Бот не отвечает
```powershell
docker logs vectora-bot-1 -f
```

### Приложение не открывается
```powershell
docker-compose ps  # Все должны быть Up
npx localtunnel --port 3000  # Перезапуск туннеля
```

### Полный перезапуск
```powershell
docker-compose down
.\start.ps1
```

---

## 💡 Советы

- **Туннель работает пока окно PowerShell открыто**
- localtunnel URL может меняться при перезапуске
- Если URL изменился → обновите Menu Button в @BotFather
- Для постоянного URL нужен production деплой ([DEPLOYMENT.md](DEPLOYMENT.md))

---

## 📚 Документация

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production VPS
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Разработка
- **[SECURITY.md](SECURITY.md)** - Безопасность

---

**Время запуска: 5-10 минут** ⏱️  
**Готово к использованию! 🚀**
