FROM python:3.11-slim

WORKDIR /app

# Копируем только requirements сначала для кэширования слоя
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы
COPY . /app

# Используем Python entrypoint
CMD ["python3", "entrypoint.py"]
