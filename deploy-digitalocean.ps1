# Автоматический деплой Vectora на DigitalOcean App Platform
# =============================================================
# Требует: GitHub Student Pack ($200 кредитов)
# Стоимость: ~$12/месяц (1 год бесплатно с кредитами)

Write-Host ""
Write-Host "╔═══════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   🌊 Vectora → DigitalOcean              ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Конфигурация
$APP_NAME = "vectora-app"
$REGION = "fra"  # Frankfurt (ближайший к России регион)
$BOT_TOKEN = "8314825408:AAHbl_06QBEG8B64FiP8Cb0YfwoaV-7H2lQ"
$GITHUB_REPO = "nelepuy/vectora"

Write-Host "📋 Конфигурация:" -ForegroundColor Yellow
Write-Host "   App Name: $APP_NAME" -ForegroundColor Gray
Write-Host "   Region: Frankfurt (fra)" -ForegroundColor Gray
Write-Host "   GitHub: $GITHUB_REPO" -ForegroundColor Gray
Write-Host ""

# Проверка doctl
Write-Host "🔍 Проверка DigitalOcean CLI..." -ForegroundColor Yellow
$doctlInstalled = Get-Command doctl -ErrorAction SilentlyContinue
if (-not $doctlInstalled) {
    Write-Host "❌ doctl не установлен!" -ForegroundColor Red
    Write-Host ""
    Write-Host "📦 Установка:" -ForegroundColor Yellow
    Write-Host "   winget install DigitalOcean.Doctl" -ForegroundColor White
    Write-Host ""
    Write-Host "   Или скачайте: https://github.com/digitalocean/doctl/releases" -ForegroundColor Gray
    Write-Host ""
    Write-Host "🎓 GitHub Student Pack:" -ForegroundColor Cyan
    Write-Host "   1. Зарегистрируйтесь: https://education.github.com/pack" -ForegroundColor White
    Write-Host "   2. Активируйте DigitalOcean ($200 кредитов)" -ForegroundColor White
    Write-Host "   3. Создайте аккаунт: https://www.digitalocean.com/" -ForegroundColor White
    Write-Host ""
    pause
    exit 1
}
Write-Host "✅ doctl установлен!" -ForegroundColor Green
Write-Host ""

# Проверка авторизации
Write-Host "🔐 Проверка авторизации..." -ForegroundColor Yellow
$authCheck = doctl auth list 2>$null
if (-not $authCheck -or $authCheck -match "no authentication contexts") {
    Write-Host "⚠️  Не авторизованы в DigitalOcean" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📝 Шаги для авторизации:" -ForegroundColor Cyan
    Write-Host "   1. Откройте: https://cloud.digitalocean.com/account/api/tokens" -ForegroundColor White
    Write-Host "   2. Нажмите 'Generate New Token'" -ForegroundColor White
    Write-Host "   3. Имя: vectora-deploy" -ForegroundColor White
    Write-Host "   4. Права: Read и Write" -ForegroundColor White
    Write-Host "   5. Скопируйте токен" -ForegroundColor White
    Write-Host ""
    $token = Read-Host "Вставьте токен сюда"
    
    doctl auth init --access-token $token
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Ошибка авторизации!" -ForegroundColor Red
        pause
        exit 1
    }
}
Write-Host "✅ Авторизация успешна!" -ForegroundColor Green
Write-Host ""

# Создание PostgreSQL Database
Write-Host "🗄️  Создание PostgreSQL Database..." -ForegroundColor Yellow
Write-Host "   (это займёт 3-5 минут)" -ForegroundColor Gray

$DB_NAME = "vectora-db"
$DB_CLUSTER = "vectora-postgres"

# Проверка существующей БД
$existingDb = doctl databases list --format Name --no-header | Select-String -Pattern $DB_CLUSTER -Quiet
if ($existingDb) {
    Write-Host "✅ База данных уже существует!" -ForegroundColor Green
} else {
    doctl databases create $DB_CLUSTER `
        --engine pg `
        --version 15 `
        --region $REGION `
        --size db-s-1vcpu-1gb `
        --num-nodes 1 2>$null
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Ошибка создания БД!" -ForegroundColor Red
        pause
        exit 1
    }
    
    Write-Host "⏳ Ожидание готовности БД..." -ForegroundColor Gray
    Start-Sleep -Seconds 60
    Write-Host "✅ База данных создана!" -ForegroundColor Green
}
Write-Host ""

# Получение данных БД
Write-Host "🔑 Получение данных БД..." -ForegroundColor Yellow
$dbInfo = doctl databases get $DB_CLUSTER --format ID,Connection --no-header 2>$null
if (-not $dbInfo) {
    Write-Host "❌ Не удалось получить данные БД!" -ForegroundColor Red
    pause
    exit 1
}

$DB_ID = ($dbInfo -split '\s+')[0]
$DB_CONNECTION = (doctl databases connection $DB_CLUSTER --format URI --no-header) -replace "defaultdb", "vectora"

Write-Host "✅ Данные БД получены!" -ForegroundColor Green
Write-Host ""

# Создание app.yaml для App Platform
Write-Host "📝 Создание конфигурации App Platform..." -ForegroundColor Yellow

$SECRET_KEY = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 64 | ForEach-Object {[char]$_})

$appYaml = @"
name: $APP_NAME
region: $REGION

databases:
- name: postgres
  engine: PG
  production: true
  cluster_name: $DB_CLUSTER

services:
# Backend API
- name: backend
  dockerfile_path: backend/Dockerfile
  source_dir: /
  github:
    repo: $GITHUB_REPO
    branch: main
    deploy_on_push: true
  
  http_port: 8000
  
  instance_count: 1
  instance_size_slug: basic-xxs
  
  envs:
  - key: DATABASE_URL
    scope: RUN_TIME
    value: `${postgres.DATABASE_URL}
  - key: SECRET_KEY
    scope: RUN_TIME
    value: $SECRET_KEY
  - key: TELEGRAM_BOT_TOKEN
    scope: RUN_TIME
    value: $BOT_TOKEN
  - key: ALLOWED_ORIGINS
    scope: RUN_TIME
    value: `${APP_URL}
  
  health_check:
    http_path: /health
    
  routes:
  - path: /api
    preserve_path_prefix: true

# Frontend React App
- name: frontend
  dockerfile_path: frontend/Dockerfile
  source_dir: /
  github:
    repo: $GITHUB_REPO
    branch: main
    deploy_on_push: true
  
  http_port: 80
  
  instance_count: 1
  instance_size_slug: basic-xxs
  
  envs:
  - key: REACT_APP_API_URL
    scope: BUILD_TIME
    value: `${backend.PUBLIC_URL}
  
  routes:
  - path: /

# Telegram Bot
- name: bot
  dockerfile_path: bot/Dockerfile
  source_dir: /
  github:
    repo: $GITHUB_REPO
    branch: main
    deploy_on_push: true
  
  http_port: 8080
  
  instance_count: 1
  instance_size_slug: basic-xxs
  
  envs:
  - key: BOT_TOKEN
    scope: RUN_TIME
    value: $BOT_TOKEN
  - key: WEBAPP_URL
    scope: RUN_TIME
    value: `${frontend.PUBLIC_URL}
  - key: API_URL
    scope: RUN_TIME
    value: `${backend.PUBLIC_URL}
"@

$appYaml | Out-File -FilePath ".do/app.yaml" -Encoding UTF8 -Force
Write-Host "✅ Конфигурация создана!" -ForegroundColor Green
Write-Host ""

# Создание приложения
Write-Host "🚀 Создание приложения..." -ForegroundColor Yellow
Write-Host "   (это займёт 5-10 минут)" -ForegroundColor Gray

$existingApp = doctl apps list --format Spec.Name --no-header | Select-String -Pattern $APP_NAME -Quiet
if ($existingApp) {
    Write-Host "⚠️  Приложение уже существует, обновляем..." -ForegroundColor Yellow
    doctl apps update $APP_NAME --spec .do/app.yaml 2>$null
} else {
    doctl apps create --spec .do/app.yaml 2>$null
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Ошибка создания приложения!" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Альтернативный способ деплоя:" -ForegroundColor Yellow
    Write-Host "   1. Откройте: https://cloud.digitalocean.com/apps" -ForegroundColor White
    Write-Host "   2. Нажмите 'Create App'" -ForegroundColor White
    Write-Host "   3. Выберите GitHub репозиторий: $GITHUB_REPO" -ForegroundColor White
    Write-Host "   4. Следуйте инструкциям в DEPLOYMENT_OPTIONS_RU.md" -ForegroundColor White
    Write-Host ""
    pause
    exit 1
}

Write-Host "✅ Приложение создано!" -ForegroundColor Green
Write-Host ""

# Ожидание деплоя
Write-Host "⏳ Ожидание завершения деплоя..." -ForegroundColor Yellow
Write-Host "   (подождите 5-10 минут)" -ForegroundColor Gray
Write-Host "   Можете следить за прогрессом: https://cloud.digitalocean.com/apps" -ForegroundColor Gray
Write-Host ""

$deployed = $false
$attempts = 0
$maxAttempts = 30

while (-not $deployed -and $attempts -lt $maxAttempts) {
    Start-Sleep -Seconds 20
    $attempts++
    
    $appStatus = doctl apps list --format Spec.Name,ActiveDeployment.Phase --no-header 2>$null | 
                 Select-String -Pattern $APP_NAME
    
    if ($appStatus -match "ACTIVE") {
        $deployed = $true
        Write-Host "✅ Деплой завершён!" -ForegroundColor Green
    } elseif ($appStatus -match "ERROR|FAILED") {
        Write-Host "❌ Ошибка деплоя!" -ForegroundColor Red
        Write-Host "   Проверьте логи: https://cloud.digitalocean.com/apps" -ForegroundColor White
        pause
        exit 1
    } else {
        Write-Host "   ⏳ Деплой в процессе... (попытка $attempts/$maxAttempts)" -ForegroundColor Gray
    }
}

if (-not $deployed) {
    Write-Host "⚠️  Деплой всё ещё в процессе" -ForegroundColor Yellow
    Write-Host "   Проверьте статус: https://cloud.digitalocean.com/apps" -ForegroundColor White
}
Write-Host ""

# Получение URL приложения
Write-Host "🌐 Получение URLs..." -ForegroundColor Yellow
$APP_URL = doctl apps list --format Spec.Name,DefaultIngress --no-header 2>$null | 
           Select-String -Pattern $APP_NAME | 
           ForEach-Object { ($_ -split '\s+')[1] }

if ($APP_URL) {
    $FRONTEND_URL = "https://$APP_URL"
    $BACKEND_URL = "https://$APP_URL/api"
    Write-Host "✅ URLs получены!" -ForegroundColor Green
} else {
    Write-Host "⚠️  URLs пока недоступны" -ForegroundColor Yellow
    $FRONTEND_URL = "https://$APP_NAME.ondigitalocean.app"
    $BACKEND_URL = "https://$APP_NAME.ondigitalocean.app/api"
}
Write-Host ""

# Итоговая информация
Write-Host ""
Write-Host "╔═══════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║          ✅ ДЕПЛОЙ ЗАВЕРШЁН!              ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Ваши URLs:" -ForegroundColor Cyan
Write-Host "   Frontend:  $FRONTEND_URL" -ForegroundColor White
Write-Host "   Backend:   $BACKEND_URL" -ForegroundColor White
Write-Host "   Dashboard: https://cloud.digitalocean.com/apps" -ForegroundColor White
Write-Host ""
Write-Host "🗄️  База данных:" -ForegroundColor Cyan
Write-Host "   Cluster:   $DB_CLUSTER" -ForegroundColor White
Write-Host "   Dashboard: https://cloud.digitalocean.com/databases" -ForegroundColor White
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
Write-Host "   # Логи приложения" -ForegroundColor Gray
Write-Host "   doctl apps logs $APP_NAME --type run" -ForegroundColor White
Write-Host ""
Write-Host "   # Статус деплоя" -ForegroundColor Gray
Write-Host "   doctl apps list" -ForegroundColor White
Write-Host ""
Write-Host "   # Перезапуск" -ForegroundColor Gray
Write-Host "   doctl apps create-deployment $APP_NAME" -ForegroundColor White
Write-Host ""
Write-Host "   # Удалить всё" -ForegroundColor Gray
Write-Host "   doctl apps delete $APP_NAME" -ForegroundColor White
Write-Host "   doctl databases delete $DB_CLUSTER" -ForegroundColor White
Write-Host ""
Write-Host "💰 Стоимость:" -ForegroundColor Magenta
Write-Host "   ~`$12/месяц (Basic Plan)" -ForegroundColor White
Write-Host "   С GitHub Student Pack: 1 год БЕСПЛАТНО (`$200 кредитов)" -ForegroundColor Green
Write-Host ""
Write-Host "🎓 GitHub Student Pack:" -ForegroundColor Cyan
Write-Host "   https://education.github.com/pack" -ForegroundColor White
Write-Host ""
Write-Host "🎉 Готово! Vectora работает на DigitalOcean!" -ForegroundColor Green
Write-Host ""

# Сохранение информации в файл
$deployInfo = @"
Vectora DigitalOcean Deployment Info
=====================================
Дата деплоя: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

URLs:
- Frontend: $FRONTEND_URL
- Backend:  $BACKEND_URL
- Dashboard: https://cloud.digitalocean.com/apps

База данных:
- Cluster: $DB_CLUSTER
- Dashboard: https://cloud.digitalocean.com/databases

DigitalOcean:
- App Name: $APP_NAME
- Region: $REGION (Frankfurt)

Telegram Bot:
- Username: @PlanerPlanerbot
- Token: $BOT_TOKEN

Menu Button URL:
$FRONTEND_URL

GitHub Student Pack:
- $200 кредитов = 1 год бесплатного хостинга
- https://education.github.com/pack
"@

$deployInfo | Out-File -FilePath "digitalocean-deploy-info.txt" -Encoding UTF8
Write-Host "💾 Информация сохранена в: digitalocean-deploy-info.txt" -ForegroundColor Cyan
Write-Host ""

pause
