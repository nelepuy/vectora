# Скрипт для запуска тестов (Windows PowerShell)

Write-Host "🧪 Запуск тестов Vectora Backend..." -ForegroundColor Cyan

# Активируем виртуальное окружение если есть
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
} elseif (Test-Path ".venv\Scripts\Activate.ps1") {
    & ".venv\Scripts\Activate.ps1"
}

# Устанавливаем зависимости для тестов
Write-Host "`nУстановка тестовых зависимостей..." -ForegroundColor Yellow
pip install -q pytest pytest-cov httpx

# Запускаем тесты
Write-Host "`nЗапуск unit тестов...`n" -ForegroundColor Yellow
pytest tests/ -v --cov=app --cov-report=term-missing

# Проверяем результат
if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Все тесты пройдены успешно!" -ForegroundColor Green
} else {
    Write-Host "`n❌ Некоторые тесты провалились" -ForegroundColor Red
    exit 1
}
