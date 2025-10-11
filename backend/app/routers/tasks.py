
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.auth import get_current_user
from typing import List, Optional

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[schemas.TaskOut])
def read_tasks(
    skip: int = Query(0, ge=0, description="Пропустить N записей"),
    limit: int = Query(100, ge=1, le=500, description="Лимит записей"),
    status: Optional[bool] = Query(None, description="Фильтр по статусу (true=выполнено, false=активно)"),
    priority: Optional[str] = Query(None, description="Фильтр по приоритету (low/normal/high)"),
    search: Optional[str] = Query(None, description="Поиск по названию и описанию"),
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    tag: Optional[str] = Query(None, description="Фильтр по тегу"),
    sort_by: Optional[str] = Query("position", description="Сортировка (position/date/priority/title)"),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    """
    Получить список задач с фильтрацией и пагинацией.
    
    - **skip**: количество пропускаемых записей
    - **limit**: максимальное количество записей
    - **status**: фильтр по статусу выполнения
    - **priority**: фильтр по приоритету
    - **search**: поиск по тексту в названии и описании
    - **category**: фильтр по категории
    - **tag**: фильтр по тегу
    - **sort_by**: сортировка (position, date, priority, title)
    """
    return crud.get_tasks(
        db=db,
        user_id=user_id,
        skip=skip,
        limit=limit,
        status=status,
        priority=priority,
        search=search,
        category=category,
        tag=tag,
        sort_by=sort_by
    )


@router.get("/{task_id}", response_model=schemas.TaskOut)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    """Получить задачу по ID."""
    return crud.get_task_by_id(db, task_id, user_id)


@router.post("/", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    """Создать новую задачу."""
    return crud.create_task(db, task, user_id)


@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    """Обновить задачу."""
    return crud.update_task(db, task_id, task, user_id)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    """Удалить задачу."""
    crud.delete_task(db, task_id, user_id)
    return None


@router.get("/metadata/categories", response_model=List[str])
def get_categories(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    """Получить список всех категорий пользователя."""
    return crud.get_categories(db, user_id)


@router.get("/metadata/tags", response_model=List[str])
def get_tags(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    """Получить список всех тегов пользователя."""
    return crud.get_all_tags(db, user_id)
