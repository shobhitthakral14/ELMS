"""
Enums used across the application
"""
from enum import Enum


class UserRole(str, Enum):
    """User roles in the system"""
    EMPLOYEE = "employee"
    MANAGER = "manager"
    HR_ADMIN = "hr_admin"


class RequestStatus(str, Enum):
    """Leave request status"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class ApprovalStatus(str, Enum):
    """Approval workflow status"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
