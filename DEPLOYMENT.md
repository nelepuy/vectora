# 🚀 Production Deployment Guide

Руководство по развертыванию Vectora в production окружении.

## 📋 Содержание

- [Требования](#требования)
- [Подготовка к деплою](#подготовка-к-деплою)
- [Варианты деплоя](#варианты-деплоя)
- [Настройка безопасности](#настройка-безопасности)
- [Мониторинг](#мониторинг)
- [Резервное копирование](#резервное-копирование)
- [Rollback процедура](#rollback-процедура)

---

## 🔧 Требования

### Минимальные системные требования

**Сервер:**
- CPU: 2+ cores
- RAM: 2GB+ (рекомендуется 4GB)
- Disk: 20GB+ SSD
- OS: Ubuntu 22.04 LTS или новее

**Программное обеспечение:**
- Docker 24.0+
- Docker Compose 2.20+
- PostgreSQL 15+
- Nginx 1.24+ (reverse proxy)
- SSL сертификат (Let's Encrypt)

### Домены

- Backend API: `api.yourdomain.com`
- Frontend: `app.yourdomain.com` (или через Telegram Web App)
- Database: приватная сеть (не публично доступна)

---

## 📦 Подготовка к деплою

### 1. Клонирование репозитория

```bash
# На production сервере
cd /opt
sudo git clone https://github.com/yourusername/Vectora.git
cd Vectora
sudo chown -R $USER:$USER .
```

### 2. Настройка переменных окружения

#### Backend (.env)

```bash
cd backend
cp .env.example .env
nano .env
```

```env
# Production настройки
APP_NAME=Vectora
APP_VERSION=0.2.0
DEBUG=false

# Database (используйте strong пароль!)
DATABASE_URL=postgresql://vectora_user:STRONG_PASSWORD_HERE@postgres:5432/vectora_prod

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather

# Security
SECRET_KEY=generate_with_openssl_rand_hex_32
ALLOWED_HOSTS=api.yourdomain.com,yourdomain.com
CORS_ORIGINS=https://app.yourdomain.com,https://web.telegram.org

# Logging
LOG_LEVEL=INFO
```

**Генерация SECRET_KEY:**
```bash
openssl rand -hex 32
```

#### Frontend (.env)

```bash
cd ../frontend
nano .env.production
```

```env
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_ENVIRONMENT=production
```

### 3. Docker Production конфигурация

Создайте `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: vectora-postgres
    restart: always
    environment:
      POSTGRES_DB: vectora_prod
      POSTGRES_USER: vectora_user
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    networks:
      - vectora-net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U vectora_user -d vectora_prod"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    container_name: vectora-backend
    restart: always
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      - DATABASE_URL=postgresql://vectora_user:${POSTGRES_PASSWORD}@postgres:5432/vectora_prod
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - DEBUG=false
    volumes:
      - ./backend/logs:/app/logs
    networks:
      - vectora-net
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
      args:
        - REACT_APP_API_URL=https://api.yourdomain.com
    container_name: vectora-frontend
    restart: always
    depends_on:
      - backend
    networks:
      - vectora-net

  nginx:
    image: nginx:1.24-alpine
    container_name: vectora-nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.prod.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - ./nginx/logs:/var/log/nginx
    depends_on:
      - backend
      - frontend
    networks:
      - vectora-net

networks:
  vectora-net:
    driver: bridge

volumes:
  postgres_data:
    driver: local
```

### 4. Production Dockerfiles

#### backend/Dockerfile.prod

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Security: создаем non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Production server
CMD ["gunicorn", "app.main:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--access-logfile", "/app/logs/access.log", \
     "--error-logfile", "/app/logs/error.log", \
     "--log-level", "info"]
```

#### frontend/Dockerfile.prod

```dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=$REACT_APP_API_URL

RUN npm run build

# Production stage
FROM nginx:1.24-alpine

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built app
COPY --from=builder /app/build /usr/share/nginx/html

# Security headers
RUN echo 'add_header X-Frame-Options "SAMEORIGIN" always;' > /etc/nginx/conf.d/security.conf && \
    echo 'add_header X-Content-Type-Options "nosniff" always;' >> /etc/nginx/conf.d/security.conf && \
    echo 'add_header X-XSS-Protection "1; mode=block" always;' >> /etc/nginx/conf.d/security.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

---

## 🌐 Варианты деплоя

### Вариант 1: VPS/Dedicated Server (DigitalOcean, Hetzner, AWS EC2)

```bash
# 1. Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 2. Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 3. Клонирование и настройка
cd /opt
git clone https://github.com/yourusername/Vectora.git
cd Vectora
# Настройте .env файлы (см. выше)

# 4. SSL сертификаты (Let's Encrypt)
sudo apt install certbot
sudo certbot certonly --standalone -d api.yourdomain.com
sudo certbot certonly --standalone -d app.yourdomain.com

# 5. Запуск
docker-compose -f docker-compose.prod.yml up -d

# 6. Проверка
docker-compose -f docker-compose.prod.yml ps
curl https://api.yourdomain.com/health
```

### Вариант 2: Kubernetes (для масштабирования)

```bash
# Coming in future versions
# See ROADMAP.md for Kubernetes deployment plans
```

### Вариант 3: Platform-as-a-Service (Heroku, Railway, Render)

**Railway.app example:**

1. Создайте новый проект на railway.app
2. Добавьте PostgreSQL service
3. Добавьте Backend service (from GitHub)
4. Добавьте Frontend service (from GitHub)
5. Настройте переменные окружения
6. Деплой происходит автоматически при push в main

---

## 🔒 Настройка безопасности

### 1. Firewall (UFW)

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 2. Fail2ban (защита от brute-force)

```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 3. PostgreSQL security

```sql
-- Создайте отдельного пользователя для приложения
CREATE USER vectora_user WITH ENCRYPTED PASSWORD 'strong_password';
CREATE DATABASE vectora_prod OWNER vectora_user;

-- Ограничьте права
GRANT CONNECT ON DATABASE vectora_prod TO vectora_user;
GRANT ALL PRIVILEGES ON DATABASE vectora_prod TO vectora_user;

-- Revoke public schema access
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO vectora_user;
```

### 4. SSL/TLS настройка Nginx

```nginx
# nginx/nginx.prod.conf
server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    location / {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name api.yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

### 5. Rate limiting

Добавьте в `backend/app/main.py`:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/tasks")
@limiter.limit("100/minute")
async def get_tasks(request: Request):
    # ...
```

---

## 📊 Мониторинг

### 1. Health check endpoint

Добавьте в `backend/app/main.py`:

```python
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check database connection
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "version": settings.app_version,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail="Service unhealthy")
```

### 2. Uptime monitoring

Используйте внешние сервисы:
- **UptimeRobot:** бесплатный мониторинг с уведомлениями
- **Pingdom:** расширенный мониторинг
- **Grafana + Prometheus:** self-hosted метрики

### 3. Логирование

```bash
# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f backend

# Логи с ротацией
# Настройте logrotate для /opt/Vectora/backend/logs/
```

### 4. Error tracking (Sentry)

```python
# backend/app/main.py
import sentry_sdk

if not settings.debug:
    sentry_sdk.init(
        dsn="your_sentry_dsn",
        environment="production",
        traces_sample_rate=0.1
    )
```

---

## 💾 Резервное копирование

### Автоматический backup PostgreSQL

Создайте `scripts/backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/opt/Vectora/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="vectora_backup_$TIMESTAMP.sql.gz"

# Создать backup
docker exec vectora-postgres pg_dump -U vectora_user vectora_prod | gzip > "$BACKUP_DIR/$BACKUP_FILE"

# Оставить только последние 7 дней
find $BACKUP_DIR -name "vectora_backup_*.sql.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_FILE"
```

Добавьте в crontab:

```bash
crontab -e
# Backup каждый день в 2:00 AM
0 2 * * * /opt/Vectora/scripts/backup.sh >> /var/log/vectora_backup.log 2>&1
```

### Восстановление из backup

```bash
# Распаковать и восстановить
gunzip -c /opt/Vectora/backups/vectora_backup_20240101_020000.sql.gz | \
docker exec -i vectora-postgres psql -U vectora_user -d vectora_prod
```

---

## ⏪ Rollback процедура

### В случае проблемного деплоя

```bash
# 1. Остановить текущую версию
cd /opt/Vectora
docker-compose -f docker-compose.prod.yml down

# 2. Откатиться на предыдущий commit
git log --oneline -n 5  # Найти нужный commit
git checkout <previous_commit_hash>

# 3. Восстановить database (если нужно)
gunzip -c /opt/Vectora/backups/vectora_backup_YYYYMMDD_HHMMSS.sql.gz | \
docker exec -i vectora-postgres psql -U vectora_user -d vectora_prod

# 4. Пересобрать и запустить
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d

# 5. Проверить health
curl https://api.yourdomain.com/health
```

---

## 📋 Deployment Checklist

Перед каждым production деплоем:

- [ ] Все тесты проходят локально
- [ ] CI/CD pipeline зеленый
- [ ] Database migrations протестированы на staging
- [ ] .env файлы обновлены с production значениями
- [ ] SSL сертификаты актуальны
- [ ] Backup создан перед деплоем
- [ ] Уведомлена команда о предстоящем деплое
- [ ] Monitoring и alerting настроены
- [ ] Rollback план подготовлен
- [ ] Post-deployment smoke tests готовы

После деплоя:

- [ ] Health check endpoint отвечает 200
- [ ] Основные функции работают (создать/прочитать задачу)
- [ ] Логи не содержат критичных ошибок
- [ ] Metrics выглядят нормально
- [ ] Telegram bot уведомления работают

---

## 🆘 Troubleshooting

### Backend не запускается

```bash
# Проверить логи
docker logs vectora-backend

# Проверить database connection
docker exec -it vectora-postgres psql -U vectora_user -d vectora_prod

# Проверить переменные окружения
docker exec vectora-backend env | grep DATABASE_URL
```

### 502 Bad Gateway

```bash
# Проверить статус backend
docker ps | grep backend

# Проверить nginx конфигурацию
docker exec vectora-nginx nginx -t

# Перезапустить nginx
docker restart vectora-nginx
```

### Database migration ошибки

```bash
# Откатить migration
docker exec vectora-backend alembic downgrade -1

# Применить заново
docker exec vectora-backend alembic upgrade head
```

---

## 📞 Support

При проблемах с production деплоем:
- GitHub Issues: https://github.com/yourusername/Vectora/issues
- Email: support@yourdomain.com

---

**Последнее обновление:** Декабрь 2024
