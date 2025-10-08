from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    date_time = Column(DateTime)
    priority = Column(String, default="normal")  # приоритет: low, normal, high
    status = Column(Boolean, default=False)
    position = Column(Integer, default=0)  # позиция для сортировки
    category = Column(String, default=None, nullable=True)  # категория задачи
    tags = Column(JSON, default=list)  # список тегов ["work", "urgent", ...]
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
