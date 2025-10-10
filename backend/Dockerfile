FROM python:3.11-slim

# CACHEBUST для форсирования пересборки
ARG CACHEBUST=2025-10-10-v5

WORKDIR /app

# Копируем только requirements сначала для кэширования слоя
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы
COPY . /app

# Делаем entrypoint исполняемым
RUN chmod +x entrypoint.py

# Railway автоматически установит переменную PORT
# КРИТИЧНО: используем exec form для правильной передачи сигналов
CMD ["python3", "-u", "entrypoint.py"]
