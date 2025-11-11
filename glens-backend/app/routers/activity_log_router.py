from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi import APIRouter, HTTPException, Depends, Query, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import get_session
from app.models.activity_log import ActivityLog, LogStatusEnum
from app.utils.log_helper import add_activity_log_async

router = APIRouter(tags=["Activity Logs"])


# -----------------------------
# 🧩 1️⃣ Fetch recent logs (default: latest 6)
# -----------------------------
@router.get("/activity-log/recent")
async def get_recent_activity_logs(
    limit: int = Query(6, ge=1, le=50),
    user_id: str | None = Query(None),
    db: AsyncSession = Depends(get_session)
):
    """
    Fetch latest activity logs (default: 6 entries).
    If user_id is provided, filter logs by user.
    """
    try:
        query = select(ActivityLog).order_by(ActivityLog.created_at.desc())

        if user_id:
            query = query.where(ActivityLog.user_id == user_id)

        query = query.limit(limit)
        result = await db.execute(query)
        logs = result.scalars().all()

        return {"logs": logs}

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database Error: {str(e)}"
        )


# -----------------------------
# 🧩 2️⃣ Add new log entry
# -----------------------------
@router.post("/activity-log/add")
async def add_activity_log_entry(
    message: str = Form(...),
    operation_type: str | None = Form(None),
    status: LogStatusEnum | None = Form(None),
    user_id: str | None = Form(None),
    db: AsyncSession = Depends(get_session)
):
    """
    Add a new activity log entry.
    Typically used for comparison start/completion/info messages.
    """
    try:
        new_log = await add_activity_log_async(
            db=db,
            message=message,
            operation_type=operation_type,
            status=status,
            user_id=user_id
        )

        if not new_log:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create activity log."
            )

        return {"success": True, "log": new_log}

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database Error: {str(e)}"
        )

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected Error: {str(e)}"
        )
