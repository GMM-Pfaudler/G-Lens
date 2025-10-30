from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
import enum

Base = declarative_base()

class StatusEnum(str, enum.Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    error = "error"

class GAGaComparisonResult(Base):
    __tablename__ = "ga_ga_comparisons"

    id = Column(Integer, primary_key=True, index=True)
    ga1_file_name = Column(String(255), nullable=False)
    ga2_file_name = Column(String(255), nullable=False)
    comparison_result_path = Column(String(512), nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.pending)
    result_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    error_msg = Column(String, nullable=True)
    job_id = Column(String(36), nullable=True, unique=True)
