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

class OFNFile(Base):
    __tablename__ = "ofn_files"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), unique=True, nullable=False)
    file_path = Column(String(512), nullable=False)
    upload_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status = Column(Enum(StatusEnum), default=StatusEnum.pending)
    error_msg = Column(String, nullable=True)


class GAFile(Base):
    __tablename__ = "ga_files"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), unique=True, nullable=False)
    file_path = Column(String(512), nullable=False)
    upload_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status = Column(Enum(StatusEnum), default=StatusEnum.pending)
    error_msg = Column(String, nullable=True)
    job_id = Column(String(36), nullable=True, unique=True)  # <-- UUID for the job


class ComparisonResult(Base):
    __tablename__ = "ofn_ga_comparisons"

    id = Column(Integer, primary_key=True, index=True)
    ofn_file_name = Column(String(255), nullable=False)
    ga_file_name = Column(String(255), nullable=False)
    comparison_result_path = Column(String(512), nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.pending)
    result_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    error_msg = Column(String, nullable=True)
    job_id = Column(String(36), nullable=True, unique=True)
