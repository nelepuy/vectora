from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    date_time: Optional[datetime] = None
    priority: Optional[str] = "normal"
    position: Optional[int] = 0

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date_time: Optional[datetime] = None
    priority: Optional[str] = None
    status: Optional[bool] = None
    position: Optional[int] = None

class TaskOut(TaskBase):
    id: int
    user_id: str
    status: bool
    created_at: datetime
    position: int
    # Для Pydantic v2: разрешаем построение из ORM-объектов
    model_config = ConfigDict(from_attributes=True)
