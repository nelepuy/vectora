from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/tasks")

# Оптимизированный engine с пулом соединений
engine = create_engine(
    DATABASE_URL,
    pool_size=10,  # Количество соединений в пуле
    max_overflow=20,  # Дополнительные соединения при необходимости
    pool_pre_ping=True,  # Проверка соединения перед использованием
    pool_recycle=3600,  # Переиспользование соединений каждый час
    echo=False  # Отключаем вывод SQL запросов в production
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
