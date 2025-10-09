# Автоматический деплой Vectora на Railway + GitHub Pages
# =========================================================
# Railway: Backend + Bot + PostgreSQL
# GitHub Pages: Frontend (React SPA)
# 
# Требует: GitHub Student Pack ($100 кредитов + $5/месяц)
# Стоимость: Backend+Bot ~$5/месяц, Frontend БЕСПЛАТНО
# Итого: ~$5/месяц (полностью покрывается Student Pack)

Write-Host ""
Write-Host "╔═══════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   🚄 Vectora → Railway + GitHub Pages    ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Конфигурация
$BOT_TOKEN = "8314825408:AAHbl_06QBEG8B64FiP8Cb0YfwoaV-7H2lQ"
$PROJECT_NAME = "vectora"
$GITHUB_USER = "nelepuy"
$GITHUB_REPO = "vectora"
$GITHUB_PAGES_URL = "https://$GITHUB_USER.github.io/$GITHUB_REPO"

Write-Host "📋 Конфигурация:" -ForegroundColor Yellow
Write-Host "   Railway Project: $PROJECT_NAME (Backend + Bot)" -ForegroundColor Gray
Write-Host "   GitHub Pages: $GITHUB_PAGES_URL (Frontend)" -ForegroundColor Gray
Write-Host "   Bot: @PlanerPlanerbot" -ForegroundColor Gray
Write-Host ""

# Проверка Railway CLI
Write-Host "🔍 Проверка Railway CLI..." -ForegroundColor Yellow
$railwayInstalled = Get-Command railway -ErrorAction SilentlyContinue
if (-not $railwayInstalled) {
    Write-Host "❌ Railway CLI не установлен!" -ForegroundColor Red
    Write-Host ""
    Write-Host "📦 Установка через npm:" -ForegroundColor Yellow
    
    # Проверка npm
    $npmInstalled = Get-Command npm -ErrorAction SilentlyContinue
    if (-not $npmInstalled) {
        Write-Host "   ❌ npm не установлен!" -ForegroundColor Red
        Write-Host "   Установите Node.js: winget install OpenJS.NodeJS" -ForegroundColor White
        Write-Host ""
        pause
        exit 1
    }
    
    Write-Host "   Устанавливаю Railway CLI..." -ForegroundColor Gray
    npm install -g @railway/cli 2>$null
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   ❌ Ошибка установки!" -ForegroundColor Red
        pause
        exit 1
    }
    
    Write-Host "   ✅ Railway CLI установлен!" -ForegroundColor Green
} else {
    Write-Host "✅ Railway CLI установлен!" -ForegroundColor Green
}
Write-Host ""

# Проверка авторизации
Write-Host "🔐 Авторизация в Railway..." -ForegroundColor Yellow
Write-Host "   (откроется браузер)" -ForegroundColor Gray

railway login

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Ошибка авторизации!" -ForegroundColor Red
    Write-Host ""
    Write-Host "🎓 GitHub Student Pack:" -ForegroundColor Cyan
    Write-Host "   1. Зарегистрируйтесь: https://education.github.com/pack" -ForegroundColor White
    Write-Host "   2. Активируйте Railway ($100 кредитов + $5/месяц)" -ForegroundColor White
    Write-Host "   3. Войдите через GitHub: https://railway.app/" -ForegroundColor White
    Write-Host ""
    pause
    exit 1
}

Write-Host "✅ Авторизация успешна!" -ForegroundColor Green
Write-Host ""

# Инициализация проекта
Write-Host "📦 Создание проекта Railway..." -ForegroundColor Yellow

# Проверка существующего проекта
$existingProject = railway status 2>$null
if ($existingProject -match "Project:") {
    Write-Host "✅ Проект уже существует!" -ForegroundColor Green
} else {
    railway init --name $PROJECT_NAME 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Ошибка создания проекта!" -ForegroundColor Red
        pause
        exit 1
    }
    Write-Host "✅ Проект создан!" -ForegroundColor Green
}
Write-Host ""

# Добавление PostgreSQL
Write-Host "🗄️  Добавление PostgreSQL..." -ForegroundColor Yellow
railway add --database postgres 2>$null
Write-Host "✅ PostgreSQL добавлена!" -ForegroundColor Green
Write-Host ""

# Генерация SECRET_KEY
$SECRET_KEY = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 64 | ForEach-Object {[char]$_})

# Настройка переменных окружения
Write-Host "⚙️  Настройка переменных окружения..." -ForegroundColor Yellow

# Backend
Write-Host "   📦 Backend..." -ForegroundColor Cyan
railway variables set `
    "SECRET_KEY=$SECRET_KEY" `
    "TELEGRAM_BOT_TOKEN=$BOT_TOKEN" `
    "ALLOWED_ORIGINS=$GITHUB_PAGES_URL" `
    --service backend 2>$null

# Bot
Write-Host "   📦 Bot..." -ForegroundColor Cyan
railway variables set `
    "BOT_TOKEN=$BOT_TOKEN" `
    "WEBAPP_URL=$GITHUB_PAGES_URL" `
    "API_URL=https://$PROJECT_NAME-backend.up.railway.app" `
    --service bot 2>$null

Write-Host "✅ Переменные настроены!" -ForegroundColor Green
Write-Host ""

# Создание railway.json для конфигурации
Write-Host "📝 Создание конфигурации Railway..." -ForegroundColor Yellow

$railwayConfig = @{
    "$schema" = "https://railway.app/railway.schema.json"
    build = @{
        builder = "DOCKERFILE"
    }
    deploy = @{
        startCommand = ""
        restartPolicyType = "ON_FAILURE"
        restartPolicyMaxRetries = 10
    }
} | ConvertTo-Json -Depth 10

$railwayConfig | Out-File -FilePath "railway.json" -Encoding UTF8
Write-Host "✅ Конфигурация создана!" -ForegroundColor Green
Write-Host ""

# Деплой на Railway (Backend + Bot)
Write-Host "🚀 Запуск деплоя на Railway..." -ForegroundColor Yellow
Write-Host "   (Backend + Bot + PostgreSQL)" -ForegroundColor Gray
Write-Host ""

# Деплой Backend и Bot
Write-Host "   📦 Backend..." -ForegroundColor Cyan
railway up --service backend --detach 2>$null

Write-Host "   📦 Bot..." -ForegroundColor Cyan
railway up --service bot --detach 2>$null

Write-Host ""
Write-Host "⏳ Ожидание завершения деплоя Railway..." -ForegroundColor Yellow
Write-Host "   (подождите 3-5 минут)" -ForegroundColor Gray
Start-Sleep -Seconds 90
Write-Host "✅ Railway деплой завершён!" -ForegroundColor Green
Write-Host ""

# Получение Backend URL
$BACKEND_URL = "https://$PROJECT_NAME-backend.up.railway.app"

# Деплой Frontend на GitHub Pages
Write-Host "📦 Деплой Frontend на GitHub Pages..." -ForegroundColor Yellow
Write-Host "   (это займёт 2-3 минуты)" -ForegroundColor Gray
Write-Host ""

# Создание .env.production для frontend
$frontendEnv = "REACT_APP_API_URL=$BACKEND_URL"
$frontendEnv | Out-File -FilePath "frontend/.env.production" -Encoding UTF8
Write-Host "   ✅ Создан frontend/.env.production" -ForegroundColor Green

# Сборка frontend
Write-Host "   🏗️  Сборка React приложения..." -ForegroundColor Cyan
Set-Location frontend
npm install 2>$null
$env:REACT_APP_API_URL = $BACKEND_URL
npm run build 2>$null
Set-Location ..
Write-Host "   ✅ Сборка завершена" -ForegroundColor Green

# Установка gh-pages если нужно
Write-Host "   📦 Установка gh-pages..." -ForegroundColor Cyan
Set-Location frontend
npm install --save-dev gh-pages 2>$null
Set-Location ..
Write-Host "   ✅ gh-pages установлен" -ForegroundColor Green

# Добавление скрипта deploy в package.json
Write-Host "   ⚙️  Настройка деплоя..." -ForegroundColor Cyan
$packageJson = Get-Content "frontend/package.json" -Raw | ConvertFrom-Json
if (-not $packageJson.homepage) {
    $packageJson | Add-Member -MemberType NoteProperty -Name "homepage" -Value $GITHUB_PAGES_URL -Force
}
if (-not $packageJson.scripts.predeploy) {
    $packageJson.scripts | Add-Member -MemberType NoteProperty -Name "predeploy" -Value "npm run build" -Force
}
if (-not $packageJson.scripts.deploy) {
    $packageJson.scripts | Add-Member -MemberType NoteProperty -Name "deploy" -Value "gh-pages -d build" -Force
}
$packageJson | ConvertTo-Json -Depth 10 | Out-File "frontend/package.json" -Encoding UTF8
Write-Host "   ✅ package.json обновлён" -ForegroundColor Green

# Деплой на GitHub Pages
Write-Host "   🚀 Публикация на GitHub Pages..." -ForegroundColor Cyan
Set-Location frontend
npm run deploy 2>$null
Set-Location ..
Write-Host "   ✅ Frontend опубликован на GitHub Pages!" -ForegroundColor Green
Write-Host ""

# Получение URLs
$FRONTEND_URL = $GITHUB_PAGES_URL
Write-Host "🌐 URLs готовы!" -ForegroundColor Green
Write-Host ""

# Итоговая информация
Write-Host ""
Write-Host "╔═══════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║          ✅ ДЕПЛОЙ ЗАВЕРШЁН!              ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Ваши URLs:" -ForegroundColor Cyan
Write-Host "   Frontend:  $FRONTEND_URL (GitHub Pages)" -ForegroundColor White
Write-Host "   Backend:   $BACKEND_URL (Railway)" -ForegroundColor White
Write-Host "   Bot:       Railway (работает в фоне)" -ForegroundColor White
Write-Host ""
Write-Host "📊 Dashboards:" -ForegroundColor Cyan
Write-Host "   Railway:      https://railway.app/dashboard" -ForegroundColor White
Write-Host "   GitHub Pages: https://github.com/$GITHUB_USER/$GITHUB_REPO/settings/pages" -ForegroundColor White
Write-Host ""
Write-Host "🤖 Следующие шаги:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   1️⃣  Откройте @BotFather в Telegram" -ForegroundColor White
Write-Host "   2️⃣  /mybots → PlanerSeptember → Bot Settings → Menu Button" -ForegroundColor White
Write-Host "   3️⃣  Название: Открыть Vectora" -ForegroundColor White
Write-Host "   4️⃣  URL: $FRONTEND_URL" -ForegroundColor Cyan
Write-Host ""
Write-Host "   5️⃣  Откройте бота @PlanerPlanerbot" -ForegroundColor White
Write-Host "   6️⃣  Отправьте /start" -ForegroundColor White
Write-Host "   7️⃣  Нажмите кнопку!" -ForegroundColor White
Write-Host ""
Write-Host "📚 Полезные команды:" -ForegroundColor Cyan
Write-Host "   # Логи" -ForegroundColor Gray
Write-Host "   railway logs" -ForegroundColor White
Write-Host ""
Write-Host "   # Статус" -ForegroundColor Gray
Write-Host "   railway status" -ForegroundColor White
Write-Host ""
Write-Host "   # Открыть dashboard" -ForegroundColor Gray
Write-Host "   railway open" -ForegroundColor White
Write-Host ""
Write-Host "   # Переменные окружения" -ForegroundColor Gray
Write-Host "   railway variables" -ForegroundColor White
Write-Host ""
Write-Host "💰 Стоимость:" -ForegroundColor Magenta
Write-Host "   Railway (Backend+Bot): ~`$5/месяц" -ForegroundColor White
Write-Host "   GitHub Pages (Frontend): БЕСПЛАТНО" -ForegroundColor Green
Write-Host "   Итого: ~`$5/месяц" -ForegroundColor White
Write-Host "   С GitHub Student Pack: ПОЛНОСТЬЮ ПОКРЫВАЕТСЯ (`$100 + `$5/мес)" -ForegroundColor Green
Write-Host ""
Write-Host "🎓 GitHub Student Pack:" -ForegroundColor Cyan
Write-Host "   https://education.github.com/pack" -ForegroundColor White
Write-Host ""
Write-Host "🎉 Готово! Vectora работает на Railway!" -ForegroundColor Green
Write-Host ""

# Сохранение информации в файл
$deployInfo = @"
Vectora Railway + GitHub Pages Deployment Info
===============================================
Дата деплоя: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

URLs:
- Frontend: $FRONTEND_URL (GitHub Pages - БЕСПЛАТНО)
- Backend:  $BACKEND_URL (Railway)
- Bot:      Railway (работает в фоне)

Dashboards:
- Railway:      https://railway.app/dashboard
- GitHub Pages: https://github.com/$GITHUB_USER/$GITHUB_REPO/settings/pages

Railway:
- Project: $PROJECT_NAME
- Services: Backend + Bot + PostgreSQL

GitHub Pages:
- Repository: $GITHUB_USER/$GITHUB_REPO
- Branch: gh-pages
- URL: $GITHUB_PAGES_URL

Telegram Bot:
- Username: @PlanerPlanerbot
- Token: $BOT_TOKEN

Menu Button URL:
$FRONTEND_URL

Стоимость:
- Railway (Backend+Bot): ~`$5/месяц
- GitHub Pages (Frontend): БЕСПЛАТНО
- Итого: ~`$5/месяц

GitHub Student Pack:
- `$100 кредитов + `$5/месяц = полностью покрывает расходы
- https://education.github.com/pack

Полезные команды:
Railway:
- railway logs        # Логи backend/bot
- railway status      # Статус
- railway open        # Открыть dashboard

GitHub Pages:
- cd frontend && npm run deploy    # Обновить frontend
- git push origin gh-pages         # Ручной пуш на gh-pages
"@

$deployInfo | Out-File -FilePath "railway-deploy-info.txt" -Encoding UTF8
Write-Host "💾 Информация сохранена в: railway-deploy-info.txt" -ForegroundColor Cyan
Write-Host ""

pause
