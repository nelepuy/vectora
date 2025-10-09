# Security checks script для PowerShell (Windows)
# VECTORA SECURITY CHECKS

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "VECTORA SECURITY CHECKS" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

# 1. Bandit - поиск уязвимостей безопасности
Write-Host "`n1. Запуск Bandit (поиск уязвимостей)..." -ForegroundColor Yellow
try {
    bandit -r app/ -c .bandit -f txt
    Write-Host "Bandit: OK" -ForegroundColor Green
} catch {
    Write-Host "Bandit: Найдены уязвимости!" -ForegroundColor Red
}

# 2. Safety - проверка зависимостей на известные уязвимости
Write-Host "`n2. Запуск Safety (проверка зависимостей)..." -ForegroundColor Yellow
try {
    safety check --json
    Write-Host "Safety: OK" -ForegroundColor Green
} catch {
    Write-Host "Safety: Найдены уязвимые зависимости!" -ForegroundColor Red
}

# 3. Flake8 - линтинг кода
Write-Host "`n3. Запуск Flake8 (линтинг)..." -ForegroundColor Yellow
try {
    flake8 app/
    Write-Host "Flake8: OK" -ForegroundColor Green
} catch {
    Write-Host "Flake8: Найдены проблемы в коде!" -ForegroundColor Red
}

# 4. MyPy - проверка типов
Write-Host "`n4. Запуск MyPy (проверка типов)..." -ForegroundColor Yellow
try {
    mypy app/
    Write-Host "MyPy: OK" -ForegroundColor Green
} catch {
    Write-Host "MyPy: Найдены проблемы с типизацией!" -ForegroundColor Red
}

# 5. Pytest - тесты безопасности
Write-Host "`n5. Запуск тестов безопасности..." -ForegroundColor Yellow
try {
    pytest tests/test_security.py -v
    Write-Host "Tests: OK" -ForegroundColor Green
} catch {
    Write-Host "Tests: Тесты не прошли!" -ForegroundColor Red
}

# 6. Проверка .env файлов
Write-Host "`n6. Проверка конфиденциальных файлов..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "ВНИМАНИЕ: Найден .env файл в репозитории!" -ForegroundColor Red
    Write-Host "Убедитесь, что он добавлен в .gitignore" -ForegroundColor Yellow
}

# Проверка жестко заданных секретов
$secrets = Get-ChildItem -Path app -Recurse -File | Select-String -Pattern "(password|secret)\s*=\s*['\"]" -SimpleMatch
if ($secrets) {
    Write-Host "ВНИМАНИЕ: Найдены жестко заданные секреты в коде!" -ForegroundColor Red
    $secrets | ForEach-Object { Write-Host $_.Line -ForegroundColor Yellow }
}

Write-Host "`n======================================" -ForegroundColor Green
Write-Host "Проверки безопасности завершены!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
