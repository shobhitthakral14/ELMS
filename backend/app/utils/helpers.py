"""
Helper utility functions
"""
from datetime import date, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from ..models import Holiday, LeaveRequest, Delegation
from ..schemas import RequestStatus


def calculate_working_days(start_date: date, end_date: date, db: Session) -> float:
    """
    Calculate working days excluding weekends and holidays
    """
    if start_date > end_date:
        raise ValueError("Start date must be before end date")

    # Get holidays in the date range
    holidays = db.query(Holiday).filter(
        Holiday.date >= start_date,
        Holiday.date <= end_date
    ).all()
    holiday_dates = {h.date for h in holidays}

    working_days = 0
    current_date = start_date

    while current_date <= end_date:
        # Skip weekends (5=Saturday, 6=Sunday)
        if current_date.weekday() < 5 and current_date not in holiday_dates:
            working_days += 1
        current_date += timedelta(days=1)

    return float(working_days)


def check_overlapping_requests(
    user_id: int,
    start_date: date,
    end_date: date,
    db: Session,
    exclude_request_id: Optional[int] = None
) -> bool:
    """
    Check if user has overlapping leave requests
    """
    query = db.query(LeaveRequest).filter(
        LeaveRequest.user_id == user_id,
        LeaveRequest.status.in_([RequestStatus.PENDING, RequestStatus.APPROVED]),
        LeaveRequest.start_date <= end_date,
        LeaveRequest.end_date >= start_date
    )

    if exclude_request_id:
        query = query.filter(LeaveRequest.id != exclude_request_id)

    return query.first() is not None


def get_active_delegate(approver_id: int, approval_date: date, db: Session) -> Optional[int]:
    """
    Get active delegate for an approver on a specific date
    """
    delegation = db.query(Delegation).filter(
        Delegation.delegator_id == approver_id,
        Delegation.is_active == True,
        Delegation.start_date <= approval_date,
        Delegation.end_date >= approval_date
    ).first()

    return delegation.delegate_id if delegation else None
