# -*- coding: utf-8 -*-
"""
Модуль аутентификации через Telegram WebApp.
Проверяет initData от Telegram Mini App на подлинность.
"""
import hashlib
import hmac
import json
from typing import Optional
from urllib.parse import parse_qsl
from fastapi import Header, HTTPException, status
from app.settings import settings


def verify_telegram_init_data(init_data: str, bot_token: str) -> dict:
    """
    Проверяет подпись initData от Telegram WebApp.
    
    Args:
        init_data: строка с данными от Telegram.WebApp.initData
        bot_token: токен бота
    
    Returns:
        dict с распарсенными данными пользователя
    
    Raises:
        HTTPException: если подпись невалидна
    """
    try:
        # Парсим query-строку
        parsed = dict(parse_qsl(init_data))
        
        # Извлекаем hash из данных
        received_hash = parsed.pop('hash', None)
        if not received_hash:
            raise ValueError("Отсутствует hash в initData")
        
        # Сортируем параметры и формируем data-check-string
        data_check_arr = [f"{k}={v}" for k, v in sorted(parsed.items())]
        data_check_string = '\n'.join(data_check_arr)
        
        # Вычисляем secret_key = HMAC-SHA256(bot_token, "WebAppData")
        secret_key = hmac.new(
            "WebAppData".encode(),
            bot_token.encode(),
            hashlib.sha256
        ).digest()
        
        # Вычисляем hash = HMAC-SHA256(data_check_string, secret_key)
        calculated_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Сравниваем хэши
        if not hmac.compare_digest(received_hash, calculated_hash):
            raise ValueError("Неверная подпись initData")
        
        # Парсим данные пользователя
        user_data = json.loads(parsed.get('user', '{}'))
        
        return {
            'user_id': str(user_data.get('id')),
            'username': user_data.get('username'),
            'first_name': user_data.get('first_name'),
            'last_name': user_data.get('last_name'),
            'language_code': user_data.get('language_code'),
            'is_premium': user_data.get('is_premium', False),
            'auth_date': parsed.get('auth_date'),
        }
    
    except (ValueError, json.JSONDecodeError, KeyError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Ошибка аутентификации: {str(e)}"
        )


async def get_current_user(
    x_telegram_init_data: Optional[str] = Header(None, alias="X-Telegram-Init-Data")
) -> str:
    """
    Dependency для получения текущего пользователя из заголовка.
    
    В разработке можно отключить проверку, установив DEBUG=true.
    В продакшене обязательно проверяет подпись Telegram.
    
    Returns:
        user_id как строка
    """
    # В режиме разработки можно пропустить аутентификацию
    if settings.debug and not x_telegram_init_data:
        return "test_user"
    
    if not x_telegram_init_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Отсутствуют данные аутентификации Telegram"
        )
    
    # Проверяем подпись через токен бота
    bot_token = settings.telegram_bot_token
    if not bot_token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не настроен токен бота"
        )
    
    user_info = verify_telegram_init_data(x_telegram_init_data, bot_token)
    return user_info['user_id']


async def get_current_user_optional(
    x_telegram_init_data: Optional[str] = Header(None, alias="X-Telegram-Init-Data")
) -> Optional[str]:
    """
    Опциональная аутентификация (не требует обязательной авторизации).
    """
    try:
        return await get_current_user(x_telegram_init_data)
    except HTTPException:
        return None
