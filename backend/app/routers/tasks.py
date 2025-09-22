
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, models, database
from typing import List

router = APIRouter(prefix="/tasks", tags=["tasks"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_id(authorization: str = None):
    # Заглушка авторизации: позже заменить на проверку initData/JWT
    return "test_user"

@router.get("/", response_model=List[schemas.TaskOut])
def read_tasks(db: Session = Depends(get_db), user_id: str = Depends(get_user_id)):
    return crud.get_tasks(db, user_id)

@router.post("/", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id)):
    return crud.create_task(db, task, user_id)

@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    return crud.update_task(db, task_id, task)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    crud.delete_task(db, task_id)
    return None
