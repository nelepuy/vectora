from pydantic import BaseModel, ConfigDict, Field, EmailStr, validator, field_validator
from typing import Optional, List
from datetime import datetime
import re

# ==================== USER SCHEMAS ====================

class UserBase(BaseModel):
    """Базовая схема пользователя"""
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: Optional[EmailStr] = Field(None, description="Email address")
    telegram_id: Optional[str] = Field(None, max_length=100)
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        """Валидация username - только буквы, цифры, подчеркивание"""
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username can only contain letters, numbers, and underscores')
        return v


class UserCreate(UserBase):
    """Схема создания пользователя"""
    password: str = Field(..., min_length=8, max_length=100, description="Password")
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Валидация пароля - минимум 8 символов, буквы и цифры"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('Password must contain at least one letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserUpdate(BaseModel):
    """Схема обновления пользователя"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100)


class UserOut(UserBase):
    """Схема вывода пользователя (без пароля!)"""
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """Схема токена"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Схема payload токена"""
    sub: Optional[int] = None
    exp: Optional[int] = None
    type: Optional[str] = None


class LoginRequest(BaseModel):
    """Схема запроса на логин"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=1, max_length=100)


# ==================== TASK SCHEMAS ====================

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500, description="Task title")
    description: Optional[str] = Field(None, max_length=5000, description="Task description")
    date_time: Optional[datetime] = None
    priority: Optional[str] = Field("normal", pattern="^(low|normal|high)$")
    position: Optional[int] = Field(0, ge=0)
    category: Optional[str] = Field(None, max_length=100)
    tags: Optional[List[str]] = Field(default_factory=list)
    
    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v):
        """Валидация тегов - максимум 10 тегов, каждый до 50 символов"""
        if v and len(v) > 10:
            raise ValueError('Maximum 10 tags allowed')
        if v:
            for tag in v:
                if len(tag) > 50:
                    raise ValueError('Each tag must be less than 50 characters')
        return v

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date_time: Optional[datetime] = None
    priority: Optional[str] = None
    status: Optional[bool] = None
    position: Optional[int] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None

class TaskOut(TaskBase):
    id: int
    user_id: int  # Теперь это integer, связь с User
    status: bool
    created_at: datetime
    position: int
    category: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    
    model_config = ConfigDict(from_attributes=True)
