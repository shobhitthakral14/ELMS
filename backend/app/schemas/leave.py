"""
Leave-related schemas for request/response validation
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import date, datetime
from typing import Optional
from .enums import RequestStatus, ApprovalStatus


# Leave Type Schemas
class LeaveTypeBase(BaseModel):
    """Base leave type schema"""
    name: str
    annual_quota: float = Field(gt=0)
    requires_documentation: bool = False
    is_paid: bool = True


class LeaveTypeCreate(LeaveTypeBase):
    """Schema for creating a leave type"""
    pass


class LeaveTypeUpdate(BaseModel):
    """Schema for updating a leave type"""
    name: Optional[str] = None
    annual_quota: Optional[float] = Field(default=None, gt=0)
    requires_documentation: Optional[bool] = None
    is_paid: Optional[bool] = None


class LeaveTypeResponse(LeaveTypeBase):
    """Schema for leave type response"""
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# Leave Balance Schemas
class LeaveBalanceResponse(BaseModel):
    """Schema for leave balance response"""
    id: int
    user_id: int
    leave_type_id: int
    leave_type_name: str
    year: int
    total_days: float
    used_days: float
    pending_days: float
    available_days: float

    model_config = ConfigDict(from_attributes=True)


# Leave Request Schemas
class LeaveRequestCreate(BaseModel):
    """Schema for creating a leave request"""
    leave_type_id: int
    start_date: date
    end_date: date
    reason: Optional[str] = None


class LeaveRequestUpdate(BaseModel):
    """Schema for updating a leave request"""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    reason: Optional[str] = None


class LeaveRequestResponse(BaseModel):
    """Schema for leave request response"""
    id: int
    user_id: int
    user_name: str
    leave_type_id: int
    leave_type_name: str
    start_date: date
    end_date: date
    total_days: float
    reason: Optional[str]
    status: RequestStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Approval Schemas
class ApprovalAction(BaseModel):
    """Schema for approval/rejection action"""
    comments: Optional[str] = None


class ApprovalWorkflowResponse(BaseModel):
    """Schema for approval workflow response"""
    id: int
    leave_request_id: int
    approver_id: int
    approver_name: str
    approval_level: int
    status: ApprovalStatus
    comments: Optional[str]
    approved_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
