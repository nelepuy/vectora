"""
Security module: JWT authentication, password hashing, and security utilities
"""
from datetime import datetime, timedelta
from typing import Optional, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import secrets
import os

# Секретные ключи (должны быть в переменных окружения)
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Настройка хеширования паролей
# Используем Argon2 как более безопасную альтернативу bcrypt
pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto",
    argon2__memory_cost=65536,  # 64 MB
    argon2__time_cost=3,  # 3 iterations
    argon2__parallelism=4,  # 4 threads
)

# Argon2 password hasher
argon2_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
    hash_len=32,
    salt_len=16,
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверка пароля с защитой от timing attacks
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """
    Хеширование пароля с использованием Argon2
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Создание JWT access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Создание JWT refresh token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> Optional[dict]:
    """
    Проверка и декодирование JWT token
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Проверяем тип токена
        if payload.get("type") != token_type:
            return None
        
        # Проверяем срок действия
        exp = payload.get("exp")
        if exp and datetime.utcnow() > datetime.fromtimestamp(exp):
            return None
        
        return payload
    except JWTError:
        return None


def generate_secure_token(length: int = 32) -> str:
    """
    Генерация криптографически стойкого случайного токена
    """
    return secrets.token_urlsafe(length)


def sanitize_string(input_str: str, max_length: int = 1000) -> str:
    """
    Санитизация строки от потенциально опасных символов
    Защита от XSS и SQL injection
    """
    if not input_str:
        return ""
    
    # Обрезаем до максимальной длины
    sanitized = input_str[:max_length]
    
    # Удаляем опасные HTML теги и JavaScript
    dangerous_patterns = [
        '<script', '</script>',
        '<iframe', '</iframe>',
        'javascript:', 'onerror=', 'onload=',
        '<object', '</object>',
        '<embed', '</embed>',
    ]
    
    sanitized_lower = sanitized.lower()
    for pattern in dangerous_patterns:
        if pattern in sanitized_lower:
            # Экранируем опасные символы
            sanitized = sanitized.replace('<', '&lt;').replace('>', '&gt;')
            break
    
    return sanitized.strip()


def is_safe_redirect_url(url: str, allowed_hosts: list = None) -> bool:
    """
    Проверка URL на безопасность для редиректа (защита от open redirect)
    """
    if not url:
        return False
    
    # Разрешаем только относительные URL или URL из белого списка
    if url.startswith('/') and not url.startswith('//'):
        return True
    
    if allowed_hosts:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc in allowed_hosts
    
    return False


class SecurityHeaders:
    """
    Security headers для защиты от различных атак
    """
    
    @staticmethod
    def get_secure_headers() -> dict:
        """
        Возвращает безопасные HTTP заголовки
        """
        return {
            # Защита от XSS
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            
            # Content Security Policy
            "Content-Security-Policy": (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self' data:; "
                "connect-src 'self'"
            ),
            
            # HTTPS enforcement
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            
            # Referrer policy
            "Referrer-Policy": "strict-origin-when-cross-origin",
            
            # Permissions policy
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
        }
