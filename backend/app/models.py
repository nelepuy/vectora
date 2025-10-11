from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    __table_args__ = ({'extend_existing': True})
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True, nullable=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = ({'extend_existing': True})
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    parent_task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text)
    date_time = Column(DateTime, index=True)
    priority = Column(String, default="normal", index=True)
    status = Column(Boolean, default=False, index=True)
    position = Column(Integer, default=0)
    category = Column(String, default=None, nullable=True, index=True)
    tags = Column(JSON, default=list)
    recurrence_type = Column(String, nullable=True)
    recurrence_interval = Column(Integer, nullable=True)
    next_occurrence = Column(DateTime, nullable=True)
    reminder_enabled = Column(Boolean, default=False)
    reminder_minutes_before = Column(Integer, default=30)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    owner = relationship("User", back_populates="tasks")
    subtasks = relationship("Task", backref="parent", remote_side=[id], cascade="all, delete-orphan")
