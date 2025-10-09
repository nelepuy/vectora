# Векторa Task Manager - Скрипт быстрого запуска
# ================================================

Write-Host ""
Write-Host "╔═══════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   🚀 Vectora Task Manager - Запуск       ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Проверка Docker
Write-Host "📦 Проверка Docker..." -ForegroundColor Yellow
$dockerRunning = docker info 2>$null
if (-not $dockerRunning) {
    Write-Host "❌ Docker не запущен!" -ForegroundColor Red
    Write-Host "   Пожалуйста, запустите Docker Desktop и попробуйте снова." -ForegroundColor White
    Write-Host ""
    pause
    exit 1
}
Write-Host "✅ Docker работает!" -ForegroundColor Green
Write-Host ""

# Проверка bot/.env
Write-Host "🔐 Проверка конфигурации бота..." -ForegroundColor Yellow
$envPath = Join-Path $PSScriptRoot "bot\.env"
if (-not (Test-Path $envPath)) {
    Write-Host "❌ Файл bot/.env не найден!" -ForegroundColor Red
    Write-Host "   Создайте файл bot/.env из bot/.env.example" -ForegroundColor White
    Write-Host ""
    pause
    exit 1
}

$envContent = Get-Content $envPath -Raw
if ($envContent -match "YOUR_BOT_TOKEN_HERE") {
    Write-Host "⚠️  ВНИМАНИЕ: Токен бота не настроен!" -ForegroundColor Red
    Write-Host ""
    Write-Host "   Пожалуйста:" -ForegroundColor Yellow
    Write-Host "   1. Создайте бота через @BotFather в Telegram" -ForegroundColor White
    Write-Host "   2. Получите токен" -ForegroundColor White
    Write-Host "   3. Откройте bot/.env и замените YOUR_BOT_TOKEN_HERE на ваш токен" -ForegroundColor White
    Write-Host ""
    Write-Host "   Подробная инструкция: LOCAL_SETUP.md" -ForegroundColor Cyan
    Write-Host ""
    pause
    exit 1
}
Write-Host "✅ Конфигурация бота найдена!" -ForegroundColor Green
Write-Host ""

# Остановка старых контейнеров
Write-Host "🛑 Остановка старых контейнеров..." -ForegroundColor Yellow
docker-compose down 2>$null
Write-Host "✅ Готово!" -ForegroundColor Green
Write-Host ""

# Запуск контейнеров
Write-Host "🚀 Запуск контейнеров..." -ForegroundColor Yellow
Write-Host "   (это может занять 30-60 секунд при первом запуске)" -ForegroundColor Gray
docker-compose up -d --build
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Ошибка при запуске контейнеров!" -ForegroundColor Red
    Write-Host ""
    pause
    exit 1
}
Write-Host "✅ Контейнеры запущены!" -ForegroundColor Green
Write-Host ""

# Ожидание запуска
Write-Host "⏳ Ожидание запуска сервисов..." -ForegroundColor Yellow
Write-Host "   Подождите 20 секунд..." -ForegroundColor Gray
for ($i = 20; $i -gt 0; $i--) {
    Write-Host -NoNewline "`r   Осталось: $i секунд... " -ForegroundColor Gray
    Start-Sleep -Seconds 1
}
Write-Host ""
Write-Host "✅ Сервисы запущены!" -ForegroundColor Green
Write-Host ""

# Применение миграций
Write-Host "📊 Применение миграций базы данных..." -ForegroundColor Yellow
$migrationOutput = docker exec vectora-backend-1 alembic upgrade head 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Миграции применены!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Миграции уже применены или произошла ошибка" -ForegroundColor Yellow
}
Write-Host ""

# Проверка статуса
Write-Host "📋 Статус контейнеров:" -ForegroundColor Yellow
docker-compose ps
Write-Host ""

# Итоговая информация
Write-Host "╔═══════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║            ✅ ВСЁ ГОТОВО!                 ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "📱 Доступы:" -ForegroundColor Cyan
Write-Host "   • Frontend:    http://localhost:3000" -ForegroundColor White
Write-Host "   • Backend API: http://localhost:8000/docs" -ForegroundColor White
Write-Host "   • PostgreSQL:  localhost:5432" -ForegroundColor White
Write-Host ""

# Запуск localtunnel
Write-Host "🌐 Запуск туннеля для Telegram Mini App..." -ForegroundColor Yellow
Write-Host ""
Write-Host "   Используем localtunnel (доступен в России)" -ForegroundColor Gray
Write-Host ""

# Проверка Node.js
$nodeInstalled = Get-Command node -ErrorAction SilentlyContinue
if (-not $nodeInstalled) {
    Write-Host "⚠️  Node.js не установлен!" -ForegroundColor Yellow
    Write-Host "   Скачайте: https://nodejs.org/" -ForegroundColor White
    Write-Host ""
    Write-Host "   После установки запустите вручную:" -ForegroundColor Cyan
    Write-Host "   npx localtunnel --port 3000" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "✅ Node.js установлен!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 Запуск localtunnel..." -ForegroundColor Cyan
    Write-Host "   (это может занять 10-15 секунд)" -ForegroundColor Gray
    Write-Host ""
    
    # Запуск localtunnel в фоне
    $tunnelJob = Start-Job -ScriptBlock {
        npx localtunnel --port 3000 2>&1
    }
    
    # Ожидание запуска
    Start-Sleep -Seconds 5
    
    # Получение URL
    $tunnelOutput = Receive-Job -Job $tunnelJob
    $tunnelUrl = $tunnelOutput | Select-String -Pattern "https://.*\.loca\.lt" | ForEach-Object { $_.Matches.Value } | Select-Object -First 1
    
    if ($tunnelUrl) {
        Write-Host "✅ Туннель запущен!" -ForegroundColor Green
        Write-Host ""
        Write-Host "╔═══════════════════════════════════════════╗" -ForegroundColor Green
        Write-Host "║  📱 ВАШ ПУБЛИЧНЫЙ URL:                   ║" -ForegroundColor Green
        Write-Host "║                                          ║" -ForegroundColor Green
        Write-Host "║  $tunnelUrl                              " -ForegroundColor Cyan
        Write-Host "║                                          ║" -ForegroundColor Green
        Write-Host "╚═══════════════════════════════════════════╝" -ForegroundColor Green
        Write-Host ""
        
        # Обновление bot/.env
        Write-Host "📝 Обновление bot/.env..." -ForegroundColor Yellow
        $envPath = Join-Path $PSScriptRoot "bot\.env"
        $envContent = Get-Content $envPath -Raw
        $envContent = $envContent -replace 'WEBAPP_URL=.*', "WEBAPP_URL=$tunnelUrl"
        Set-Content -Path $envPath -Value $envContent -NoNewline
        Write-Host "✅ bot/.env обновлён!" -ForegroundColor Green
        Write-Host ""
        
        # Перезапуск бота
        Write-Host "🔄 Перезапуск бота..." -ForegroundColor Yellow
        docker-compose restart bot | Out-Null
        Start-Sleep -Seconds 3
        Write-Host "✅ Бот перезапущен!" -ForegroundColor Green
        Write-Host ""
    } else {
        Write-Host "⚠️  Не удалось автоматически запустить туннель" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "   Запустите вручную в НОВОМ окне PowerShell:" -ForegroundColor Cyan
        Write-Host "   npx localtunnel --port 3000" -ForegroundColor White
        Write-Host ""
    }
}

Write-Host ""
Write-Host "📍 Следующие шаги:" -ForegroundColor Cyan
Write-Host ""
Write-Host "   1️⃣  Скопируйте URL выше (https://...loca.lt)" -ForegroundColor White
Write-Host ""
Write-Host "   2️⃣  Откройте @BotFather в Telegram" -ForegroundColor White
Write-Host ""
Write-Host "   3️⃣  Настройте Menu Button:" -ForegroundColor White
Write-Host "       /mybots → Выберите бота → Bot Settings → Menu Button" -ForegroundColor Gray
Write-Host "       Название: Открыть Vectora" -ForegroundColor Gray
Write-Host "       URL: (вставьте ваш URL)" -ForegroundColor Gray
Write-Host ""
Write-Host "   4️⃣  Откройте бота в Telegram и нажмите /start!" -ForegroundColor White
Write-Host ""
Write-Host "� Совет: Туннель работает пока это окно открыто!" -ForegroundColor Cyan
Write-Host ""
Write-Host "╔═══════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║  💡 Полезные команды:                    ║" -ForegroundColor Magenta
Write-Host "╚═══════════════════════════════════════════╝" -ForegroundColor Magenta
Write-Host "   docker-compose ps        - Статус" -ForegroundColor White
Write-Host "   docker-compose logs -f   - Логи всех сервисов" -ForegroundColor White
Write-Host "   docker logs vectora-bot-1 -f  - Логи бота" -ForegroundColor White
Write-Host "   docker-compose down      - Остановить всё" -ForegroundColor White
Write-Host "   docker-compose restart bot - Перезапустить бота" -ForegroundColor White
Write-Host ""

pause
