FROM python:3.11-slim

WORKDIR /app

# Копируем всё сразу (без оптимизации кэша)
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# CMD будет переопределён через railway.toml startCommand
