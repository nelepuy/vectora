FROM python:3.11-slim

ARG CACHEBUST=fix-host-header-20251011

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# КРИТИЧНО: добавляем флаги для работы за Railway proxy
CMD uvicorn app.main_simple:app --host 0.0.0.0 --port 8080 --proxy-headers --forwarded-allow-ips "*"
