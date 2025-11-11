from sqlalchemy import Column, Integer, Text, String, Enum, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class LogStatusEnum(enum.Enum):
    started = "started"
    completed = "completed"
    error = "error"
    info = "info"

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(String(255), nullable=True)  # ✅ Added field
    message = Column(Text, nullable=False)
    operation_type = Column(String(100), nullable=True)
    status = Column(Enum(LogStatusEnum), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self):
        return (
            f"<ActivityLog(user_id='{self.user_id}', "
            f"message='{self.message[:30]}', "
            f"status='{self.status.value if self.status else None}')>"
        )
