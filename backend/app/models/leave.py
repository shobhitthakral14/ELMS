"""
Leave-related models
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base
from ..schemas.enums import RequestStatus, ApprovalStatus


class LeaveType(Base):
    """Different types of leaves (Annual, Sick, etc.)"""
    __tablename__ = "leave_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    annual_quota = Column(Float, nullable=False)
    requires_documentation = Column(Boolean, default=False)
    is_paid = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)

    # Relationships
    leave_balances = relationship("LeaveBalance", back_populates="leave_type")
    leave_requests = relationship("LeaveRequest", back_populates="leave_type")


class LeaveBalance(Base):
    """Leave balance tracking for each user"""
    __tablename__ = "leave_balances"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    leave_type_id = Column(Integer, ForeignKey("leave_types.id"), nullable=False)
    year = Column(Integer, nullable=False)
    total_days = Column(Float, nullable=False)
    used_days = Column(Float, default=0)
    pending_days = Column(Float, default=0)

    # Relationships
    user = relationship("User", back_populates="leave_balances")
    leave_type = relationship("LeaveType", back_populates="leave_balances")

    @property
    def available_days(self) -> float:
        """Calculate available leave days"""
        return self.total_days - self.used_days - self.pending_days


class LeaveRequest(Base):
    """Leave request submitted by employees"""
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    leave_type_id = Column(Integer, ForeignKey("leave_types.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    total_days = Column(Float, nullable=False)
    reason = Column(String, nullable=True)
    status = Column(SQLEnum(RequestStatus), default=RequestStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="leave_requests")
    leave_type = relationship("LeaveType", back_populates="leave_requests")
    approval_workflow = relationship("ApprovalWorkflow", back_populates="leave_request")


class ApprovalWorkflow(Base):
    """Multi-level approval workflow for leave requests"""
    __tablename__ = "approval_workflow"

    id = Column(Integer, primary_key=True, index=True)
    leave_request_id = Column(Integer, ForeignKey("leave_requests.id"), nullable=False)
    approver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    approval_level = Column(Integer, nullable=False)
    status = Column(SQLEnum(ApprovalStatus), default=ApprovalStatus.PENDING)
    comments = Column(String, nullable=True)
    approved_at = Column(DateTime, nullable=True)

    # Relationships
    leave_request = relationship("LeaveRequest", back_populates="approval_workflow")
    approver = relationship("User")
