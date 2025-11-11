from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.activity_log import ActivityLog, LogStatusEnum
from sqlalchemy.exc import SQLAlchemyError

# -----------------------------
# Sync version (if you're using normal Session)
# -----------------------------
def add_activity_log(db: Session, message: str, operation_type: str = None, status: LogStatusEnum = None, user_id: str = None):
    """
    Create a new activity log entry (sync version).
    """
    try:
        log_entry = ActivityLog(
            user_id=user_id,
            message=message,
            operation_type=operation_type,
            status=status
        )
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        return log_entry

    except SQLAlchemyError as e:
        db.rollback()
        print(f"⚠️ Database error in add_activity_log: {e}")
        return None


# -----------------------------
# Async version (if using AsyncSession)
# -----------------------------
async def add_activity_log_async(db: AsyncSession, message: str, operation_type: str = None, status: LogStatusEnum = None, user_id: str = None):
    """
    Create a new activity log entry (async version).
    """
    try:
        log_entry = ActivityLog(
            user_id=user_id,
            message=message,
            operation_type=operation_type,
            status=status
        )
        db.add(log_entry)
        await db.commit()
        await db.refresh(log_entry)
        return log_entry

    except SQLAlchemyError as e:
        await db.rollback()
        print(f"⚠️ Database error in add_activity_log_async: {e}")
        return None
