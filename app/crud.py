from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from . import models, schemas
from .exceptions import TaskNotFoundError
from typing import List, Optional
from datetime import datetime

def get_tasks(
    db: Session, 
    user_id: str,
    skip: int = 0,
    limit: int = 100,
    status: Optional[bool] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
    category: Optional[str] = None,
    tag: Optional[str] = None,
    sort_by: Optional[str] = "position"  # position, date, priority, title
) -> List[models.Task]:
    """Получить задачи с фильтрацией и пагинацией."""
    query = db.query(models.Task).filter(models.Task.user_id == user_id)
    
    # Фильтр по статусу
    if status is not None:
        query = query.filter(models.Task.status == status)
    
    # Фильтр по приоритету
    if priority:
        query = query.filter(models.Task.priority == priority)
    
    # Фильтр по категории
    if category:
        query = query.filter(models.Task.category == category)
    
    # Фильтр по тегу (проверяем наличие в JSON массиве)
    if tag:
        query = query.filter(models.Task.tags.contains([tag]))
    
    # Поиск по названию и описанию
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                models.Task.title.ilike(search_pattern),
                models.Task.description.ilike(search_pattern)
            )
        )
    
    # Сортировка
    if sort_by == "date":
        query = query.order_by(models.Task.date_time.desc().nullslast())
    elif sort_by == "priority":
        # Сортировка: high -> normal -> low
        priority_order = {"high": 1, "normal": 2, "low": 3}
        query = query.order_by(
            models.Task.priority.desc()  # Временно, можно улучшить
        )
    elif sort_by == "title":
        query = query.order_by(models.Task.title.asc())
    else:  # position (default)
        query = query.order_by(models.Task.position, models.Task.created_at.desc())
    
    return query.offset(skip).limit(limit).all()


def get_task_by_id(db: Session, task_id: int, user_id: str) -> models.Task:
    """Получить задачу по ID с проверкой владельца."""
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == user_id
    ).first()
    
    if not task:
        raise TaskNotFoundError(task_id)
    
    return task


def create_task(db: Session, task: schemas.TaskCreate, user_id: str) -> models.Task:
    """Создать новую задачу."""
    db_task = models.Task(**task.model_dump(), user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task: schemas.TaskUpdate, user_id: str) -> models.Task:
    """Обновить задачу."""
    db_task = get_task_by_id(db, task_id, user_id)
    
    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int, user_id: str):
    """Удалить задачу."""
    db_task = get_task_by_id(db, task_id, user_id)
    db.delete(db_task)
    db.commit()


def get_categories(db: Session, user_id: str) -> List[str]:
    """Получить список всех категорий пользователя."""
    tasks = db.query(models.Task).filter(
        models.Task.user_id == user_id,
        models.Task.category.isnot(None)
    ).all()
    
    categories = set()
    for task in tasks:
        if task.category:
            categories.add(task.category)
    
    return sorted(list(categories))


def get_all_tags(db: Session, user_id: str) -> List[str]:
    """Получить список всех тегов пользователя."""
    tasks = db.query(models.Task).filter(
        models.Task.user_id == user_id
    ).all()
    
    tags = set()
    for task in tasks:
        if task.tags:
            tags.update(task.tags)
    
    return sorted(list(tags))
