#!/bin/bash
# Security checks script - запуск всех проверок безопасности

echo "======================================"
echo "VECTORA SECURITY CHECKS"
echo "======================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install dependencies if needed
echo -e "${YELLOW}Проверка зависимостей...${NC}"
if ! command_exists bandit; then
    echo "Установка bandit..."
    pip install bandit
fi

if ! command_exists safety; then
    echo "Установка safety..."
    pip install safety
fi

# 1. Bandit - поиск уязвимостей безопасности
echo -e "\n${YELLOW}1. Запуск Bandit (поиск уязвимостей)...${NC}"
bandit -r app/ -c .bandit -f txt || echo -e "${RED}Найдены уязвимости!${NC}"

# 2. Safety - проверка зависимостей на известные уязвимости
echo -e "\n${YELLOW}2. Запуск Safety (проверка зависимостей)...${NC}"
safety check --json || echo -e "${RED}Найдены уязвимые зависимости!${NC}"

# 3. Flake8 - линтинг кода
echo -e "\n${YELLOW}3. Запуск Flake8 (линтинг)...${NC}"
flake8 app/ || echo -e "${RED}Найдены проблемы в коде!${NC}"

# 4. MyPy - проверка типов
echo -e "\n${YELLOW}4. Запуск MyPy (проверка типов)...${NC}"
mypy app/ || echo -e "${RED}Найдены проблемы с типизацией!${NC}"

# 5. Pylint - качество кода
echo -e "\n${YELLOW}5. Запуск Pylint (качество кода)...${NC}"
pylint app/ || echo -e "${RED}Найдены проблемы качества!${NC}"

# 6. Pytest - тесты безопасности
echo -e "\n${YELLOW}6. Запуск тестов безопасности...${NC}"
pytest tests/test_security.py -v || echo -e "${RED}Тесты не прошли!${NC}"

# 7. Проверка .env файлов
echo -e "\n${YELLOW}7. Проверка конфиденциальных файлов...${NC}"
if [ -f ".env" ]; then
    echo -e "${RED}ВНИМАНИЕ: Найден .env файл в репозитории!${NC}"
    echo "Убедитесь, что он добавлен в .gitignore"
fi

if grep -r "password\s*=\s*['\"]" app/ 2>/dev/null; then
    echo -e "${RED}ВНИМАНИЕ: Найдены жестко заданные пароли в коде!${NC}"
fi

if grep -r "secret\s*=\s*['\"]" app/ 2>/dev/null; then
    echo -e "${RED}ВНИМАНИЕ: Найдены секретные ключи в коде!${NC}"
fi

echo -e "\n${GREEN}======================================"
echo "Проверки безопасности завершены!"
echo -e "======================================${NC}"
