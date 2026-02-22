"""
User model
"""
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import date
from ..database import Base
from ..schemas.enums import UserRole


class User(Base):
    """User model for employees, managers, and HR admins"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.EMPLOYEE, nullable=False)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    department = Column(String, nullable=True)
    hire_date = Column(Date, default=date.today)
    is_active = Column(Boolean, default=True)

    # Relationships
    manager = relationship("User", remote_side=[id], backref="team_members")
    leave_balances = relationship("LeaveBalance", back_populates="user")
    leave_requests = relationship("LeaveRequest", back_populates="user")
