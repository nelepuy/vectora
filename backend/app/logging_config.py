# -*- coding: utf-8 -*-
"""
Настройка логирования для приложения.
"""
import logging
import sys
from app.settings import settings

# Формат логов
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Уровень логирования в зависимости от режима
LOG_LEVEL = logging.DEBUG if settings.debug else logging.INFO


def setup_logging():
    """Настройка системы логирования."""
    # Базовая конфигурация
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Отключаем излишне многословные логи библиотек
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    
    logger = logging.getLogger("vectora")
    logger.setLevel(LOG_LEVEL)
    
    return logger


# Глобальный logger для приложения
logger = setup_logging()
