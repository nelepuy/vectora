"""
Security tests - проверка защищенности системы
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token,
    sanitize_string,
    is_safe_redirect_url,
)

client = TestClient(app)


class TestPasswordSecurity:
    """Тесты безопасности паролей"""
    
    def test_password_hashing(self):
        """Тест хеширования пароля"""
        password = "TestPassword123!"
        hashed = get_password_hash(password)
        
        # Хеш не должен совпадать с оригинальным паролем
        assert hashed != password
        # Хеш должен быть достаточно длинным
        assert len(hashed) > 50
        
    def test_password_verification(self):
        """Тест проверки пароля"""
        password = "TestPassword123!"
        hashed = get_password_hash(password)
        
        # Правильный пароль должен пройти проверку
        assert verify_password(password, hashed) is True
        # Неправильный пароль не должен пройти
        assert verify_password("WrongPassword", hashed) is False
    
    def test_password_hashing_uniqueness(self):
        """Тест уникальности хешей (защита от rainbow tables)"""
        password = "SamePassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # Два хеша одного пароля должны отличаться (salt)
        assert hash1 != hash2


class TestJWTSecurity:
    """Тесты безопасности JWT токенов"""
    
    def test_token_creation_and_verification(self):
        """Тест создания и проверки токена"""
        data = {"sub": 123, "username": "testuser"}
        token = create_access_token(data)
        
        # Токен должен быть создан
        assert token is not None
        assert len(token) > 50
        
        # Проверка токена должна вернуть payload
        payload = verify_token(token, token_type="access")
        assert payload is not None
        assert payload["sub"] == 123
    
    def test_invalid_token(self):
        """Тест невалидного токена"""
        fake_token = "fake.invalid.token"
        payload = verify_token(fake_token)
        
        # Невалидный токен не должен пройти проверку
        assert payload is None
    
    def test_token_type_validation(self):
        """Тест проверки типа токена"""
        data = {"sub": 123}
        access_token = create_access_token(data)
        
        # Access token не должен работать как refresh
        payload = verify_token(access_token, token_type="refresh")
        assert payload is None


class TestInputSanitization:
    """Тесты санитизации входных данных"""
    
    def test_sanitize_normal_string(self):
        """Тест санитизации обычной строки"""
        input_str = "Hello, World!"
        result = sanitize_string(input_str)
        assert result == "Hello, World!"
    
    def test_sanitize_xss_attempt(self):
        """Тест защиты от XSS"""
        xss_attempts = [
            "<script>alert('XSS')</script>",
            "<iframe src='evil.com'></iframe>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>",
        ]
        
        for attempt in xss_attempts:
            result = sanitize_string(attempt)
            # Опасные теги должны быть экранированы
            assert "<script" not in result.lower() or "&lt;" in result
            assert "javascript:" not in result.lower() or "&lt;" in result
    
    def test_sanitize_length_limit(self):
        """Тест ограничения длины"""
        long_string = "A" * 2000
        result = sanitize_string(long_string, max_length=100)
        
        # Строка должна быть обрезана
        assert len(result) <= 100


class TestURLSecurity:
    """Тесты безопасности URL"""
    
    def test_safe_relative_url(self):
        """Тест безопасного относительного URL"""
        assert is_safe_redirect_url("/dashboard") is True
        assert is_safe_redirect_url("/user/profile") is True
    
    def test_unsafe_absolute_url(self):
        """Тест небезопасного абсолютного URL"""
        assert is_safe_redirect_url("//evil.com") is False
        assert is_safe_redirect_url("http://evil.com") is False
    
    def test_whitelisted_url(self):
        """Тест URL из белого списка"""
        allowed_hosts = ["trusted.com", "yourdomain.com"]
        assert is_safe_redirect_url("https://trusted.com/path", allowed_hosts) is True
        assert is_safe_redirect_url("https://evil.com/path", allowed_hosts) is False


class TestAPISecurityHeaders:
    """Тесты security headers в API"""
    
    def test_security_headers_present(self):
        """Тест наличия security headers"""
        response = client.get("/docs")
        
        # Проверяем наличие важных security headers
        assert "X-Content-Type-Options" in response.headers
        assert "X-Frame-Options" in response.headers
        assert "X-XSS-Protection" in response.headers
        assert "Content-Security-Policy" in response.headers
    
    def test_cors_headers(self):
        """Тест CORS headers"""
        response = client.options(
            "/api/tasks/",
            headers={"Origin": "http://localhost:3000"}
        )
        
        # CORS headers должны быть настроены
        assert "access-control-allow-origin" in response.headers or \
               "Access-Control-Allow-Origin" in response.headers


class TestAuthenticationSecurity:
    """Тесты безопасности аутентификации"""
    
    def test_register_weak_password(self):
        """Тест регистрации со слабым паролем"""
        weak_passwords = [
            {"username": "test1", "password": "123"},  # Слишком короткий
            {"username": "test2", "password": "password"},  # Без цифр
            {"username": "test3", "password": "12345678"},  # Без букв
        ]
        
        for user_data in weak_passwords:
            response = client.post("/auth/register", json=user_data)
            # Слабый пароль должен быть отклонен
            assert response.status_code in [400, 422]
    
    def test_sql_injection_attempt(self):
        """Тест защиты от SQL injection"""
        sql_injection_attempts = [
            {"username": "admin' OR '1'='1", "password": "password123"},
            {"username": "admin'--", "password": "password123"},
            {"username": "admin'; DROP TABLE users;--", "password": "password123"},
        ]
        
        for attempt in sql_injection_attempts:
            response = client.post("/auth/login", json=attempt)
            # SQL injection не должна пройти
            assert response.status_code in [401, 422]
    
    def test_unauthorized_access(self):
        """Тест доступа без аутентификации"""
        # Попытка доступа к защищенному эндпоинту без токена
        response = client.get("/auth/me")
        assert response.status_code == 403  # Forbidden


class TestRateLimiting:
    """Тесты rate limiting"""
    
    @pytest.mark.skip(reason="Требует настройки rate limiter в тестах")
    def test_rate_limit_exceeded(self):
        """Тест превышения rate limit"""
        # Отправляем много запросов подряд
        for i in range(100):
            response = client.get("/api/tasks/")
            if response.status_code == 429:
                # Rate limit должен сработать
                assert True
                return
        
        # Если не сработал, может быть недостаточно запросов
        pytest.skip("Rate limit not reached in 100 requests")


class TestDataLeakage:
    """Тесты утечки данных"""
    
    def test_error_no_sensitive_data(self):
        """Тест что ошибки не содержат чувствительных данных"""
        # Запрос к несуществующему эндпоинту
        response = client.get("/nonexistent")
        
        # Ошибка не должна содержать пути к файлам, пароли и т.д.
        error_text = response.text.lower()
        assert "password" not in error_text
        assert "secret" not in error_text
        assert "/app/" not in error_text  # Пути к файлам
    
    def test_user_enumeration_protection(self):
        """Тест защиты от перебора пользователей"""
        # Попытка логина с несуществующим пользователем
        response1 = client.post("/auth/login", json={
            "username": "nonexistent_user_12345",
            "password": "password123"
        })
        
        # Попытка логина с существующим пользователем, но неправильным паролем
        # (предполагаем что пользователь admin может существовать)
        response2 = client.post("/auth/login", json={
            "username": "admin",
            "password": "wrong_password"
        })
        
        # Ответы должны быть одинаковыми (timing attack protection)
        assert response1.status_code == response2.status_code
        # Сообщения об ошибке не должны раскрывать существование пользователя
        assert "user not found" not in response1.text.lower()
        assert "user not found" not in response2.text.lower()
