from sqlalchemy import Column, Integer, String, Enum, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class UserRole(enum.Enum):
    admin = "admin"
    reviewer = "reviewer"
    engineer = "engineer"
    viewer = "viewer"


class Login(Base):
    __tablename__ = "login"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.viewer)
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self):
        return f"<Login(user_id='{self.user_id}', role='{self.role.value}')>"
