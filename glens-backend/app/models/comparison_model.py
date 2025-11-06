from sqlalchemy import (
    Column, Integer, String, DateTime, Enum, ForeignKey, Text
)
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
import enum

Base = declarative_base()

class StatusEnum(str, enum.Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    error = "error"

class ComparisonResult(Base):
    __tablename__ = "ofn_ga_comparisons"

    id = Column(Integer, primary_key=True, index=True)
    ofn_file_name = Column(String(255), nullable=False)
    ga_file_name = Column(String(255), nullable=False)
    comparison_result_path = Column(String(512), nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.pending)
    error_msg = Column(Text, nullable=True)
    job_id = Column(String(36), nullable=True, unique=True)
    user_id = Column(String(255),nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
