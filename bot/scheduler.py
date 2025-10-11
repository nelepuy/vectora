import asyncio
import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.models import Task
from bot.bot import send_reminder
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/tasks")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


async def check_reminders():
    """Check for tasks that need reminders"""
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        
        tasks = db.query(Task).filter(
            and_(
                Task.reminder_enabled == True,
                Task.status == False,
                Task.date_time != None,
                Task.date_time > now
            )
        ).all()
        
        for task in tasks:
            reminder_time = task.date_time - timedelta(minutes=task.reminder_minutes_before or 30)
            
            if now >= reminder_time and now < task.date_time:
                await send_reminder(task.user_id, task.title, task.id)
                
    except Exception as e:
        print(f"Error checking reminders: {e}")
    finally:
        db.close()


async def scheduler_loop():
    """Main scheduler loop"""
    print("Reminder scheduler started")
    while True:
        await check_reminders()
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(scheduler_loop())
