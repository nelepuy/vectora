from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.auth import get_current_user
from app.models import Task
from datetime import datetime, timedelta
from typing import Dict, List

router = APIRouter(prefix="/stats", tags=["statistics"])


@router.get("/overview")
def get_stats_overview(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict:
    total = db.query(Task).filter(Task.user_id == user_id, Task.parent_task_id == None).count()
    completed = db.query(Task).filter(Task.user_id == user_id, Task.status == True, Task.parent_task_id == None).count()
    pending = total - completed
    
    today = datetime.utcnow().date()
    today_tasks = db.query(Task).filter(
        Task.user_id == user_id,
        func.date(Task.date_time) == today,
        Task.parent_task_id == None
    ).count()
    
    overdue = db.query(Task).filter(
        Task.user_id == user_id,
        Task.status == False,
        Task.date_time < datetime.utcnow(),
        Task.parent_task_id == None
    ).count()
    
    by_priority = db.query(Task.priority, func.count(Task.id)).filter(
        Task.user_id == user_id,
        Task.parent_task_id == None
    ).group_by(Task.priority).all()
    
    by_category = db.query(Task.category, func.count(Task.id)).filter(
        Task.user_id == user_id,
        Task.parent_task_id == None,
        Task.category != None
    ).group_by(Task.category).all()
    
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "today": today_tasks,
        "overdue": overdue,
        "completion_rate": round((completed / total * 100) if total > 0 else 0, 1),
        "by_priority": {priority: count for priority, count in by_priority},
        "by_category": {category: count for category, count in by_category}
    }


@router.get("/weekly")
def get_weekly_stats(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict:
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)
    
    daily_stats = []
    for i in range(7):
        date = week_ago + timedelta(days=i)
        completed_count = db.query(Task).filter(
            Task.user_id == user_id,
            func.date(Task.updated_at) == date,
            Task.status == True
        ).count()
        created_count = db.query(Task).filter(
            Task.user_id == user_id,
            func.date(Task.created_at) == date
        ).count()
        
        daily_stats.append({
            "date": date.isoformat(),
            "completed": completed_count,
            "created": created_count
        })
    
    return {"daily": daily_stats}
