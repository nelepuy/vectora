# -*- coding: utf-8 -*-
"""
Тесты для модуля аутентификации.
"""
import pytest
from app.auth import verify_telegram_init_data
from fastapi import HTTPException


def test_verify_telegram_init_data_invalid_hash():
    """Тест проверки невалидной подписи."""
    invalid_data = "hash=invalid&user=%7B%22id%22%3A123%7D"
    bot_token = "test_token"
    
    with pytest.raises(HTTPException) as exc_info:
        verify_telegram_init_data(invalid_data, bot_token)
    
    assert exc_info.value.status_code == 401


def test_verify_telegram_init_data_missing_hash():
    """Тест проверки данных без hash."""
    data_without_hash = "user=%7B%22id%22%3A123%7D"
    bot_token = "test_token"
    
    with pytest.raises(HTTPException) as exc_info:
        verify_telegram_init_data(data_without_hash, bot_token)
    
    assert exc_info.value.status_code == 401
    assert "hash" in str(exc_info.value.detail).lower()
