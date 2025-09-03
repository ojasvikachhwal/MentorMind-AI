"""
Weekly Report Scheduler Task
Automated task to send weekly progress reports to all users.
"""

import logging
from datetime import datetime
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.email_service import WeeklyReportScheduler

logger = logging.getLogger(__name__)

def send_weekly_reports_task():
    """Task to send weekly progress reports to all users."""
    db = SessionLocal()
    try:
        scheduler = WeeklyReportScheduler(db)
        result = scheduler.send_weekly_reports()
        
        logger.info(f"Weekly reports task completed: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error in weekly reports task: {e}")
        return {"sent": 0, "failed": 0}
    finally:
        db.close()

if __name__ == "__main__":
    # Run the task directly for testing
    result = send_weekly_reports_task()
    print(f"Weekly reports sent: {result['sent']}, failed: {result['failed']}")
