#!/bin/bash
# Скрипт для запуска тестов

echo "🧪 Запуск тестов Vectora Backend..."

# Активируем виртуальное окружение если есть
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Устанавливаем зависимости для тестов
pip install -q pytest pytest-cov httpx

# Запускаем тесты
echo ""
echo "Запуск unit тестов..."
pytest tests/ -v --cov=app --cov-report=term-missing

# Проверяем результат
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Все тесты пройдены успешно!"
else
    echo ""
    echo "❌ Некоторые тесты провалились"
    exit 1
fi
