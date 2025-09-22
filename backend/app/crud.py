from sqlalchemy.orm import Session
from . import models, schemas
from typing import List

def get_tasks(db: Session, user_id: str) -> List[models.Task]:
    return db.query(models.Task).filter(models.Task.user_id == user_id).all()

def create_task(db: Session, task: schemas.TaskCreate, user_id: str) -> models.Task:
    db_task = models.Task(**task.dict(), user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: schemas.TaskUpdate) -> models.Task:
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    db.delete(db_task)
    db.commit()
