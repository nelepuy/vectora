FROM python:3.11-slim

WORKDIR /app

# Копируем только requirements сначала для кэширования слоя
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы
COPY . /app

# Делаем Python скрипт запуска исполняемым
RUN chmod +x start.py

# Используем Python скрипт для запуска с миграциями
CMD ["python", "start.py"]
