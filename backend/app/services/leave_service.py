"""
Leave management service
"""
from datetime import datetime, date
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models import User, LeaveRequest, LeaveBalance, ApprovalWorkflow
from ..schemas import UserRole, RequestStatus, ApprovalStatus
from ..utils.helpers import get_active_delegate


def create_approval_workflow(leave_request: LeaveRequest, db: Session):
    """
    Create multi-level approval workflow for a leave request
    - Employee leaves: Approved by Manager
    - Manager leaves: Approved by HR Admin
    """
    user = leave_request.user
    approval_level = 1

    # Check if user is a manager
    if user.role == UserRole.MANAGER:
        # Managers' leaves go directly to HR Admin for approval
        hr_admin = db.query(User).filter(
            User.role == UserRole.HR_ADMIN,
            User.is_active == True
        ).first()
        if hr_admin:
            workflow = ApprovalWorkflow(
                leave_request_id=leave_request.id,
                approver_id=hr_admin.id,
                approval_level=approval_level,
                status=ApprovalStatus.PENDING
            )
            db.add(workflow)
    else:
        # Employee leaves: Level 1 - Direct Manager
        if user.manager_id:
            workflow = ApprovalWorkflow(
                leave_request_id=leave_request.id,
                approver_id=user.manager_id,
                approval_level=approval_level,
                status=ApprovalStatus.PENDING
            )
            db.add(workflow)
            approval_level += 1

            # Level 2: Manager's Manager (if exists)
            manager = db.query(User).filter(User.id == user.manager_id).first()
            if manager and manager.manager_id:
                workflow = ApprovalWorkflow(
                    leave_request_id=leave_request.id,
                    approver_id=manager.manager_id,
                    approval_level=approval_level,
                    status=ApprovalStatus.PENDING
                )
                db.add(workflow)
                approval_level += 1

        # Level 3: HR Admin (for leaves > 5 days)
        if leave_request.total_days > 5:
            hr_admin = db.query(User).filter(
                User.role == UserRole.HR_ADMIN,
                User.is_active == True
            ).first()
            if hr_admin:
                workflow = ApprovalWorkflow(
                    leave_request_id=leave_request.id,
                    approver_id=hr_admin.id,
                    approval_level=approval_level,
                    status=ApprovalStatus.PENDING
                )
                db.add(workflow)

    db.commit()


def process_approval(
    leave_request_id: int,
    approver_id: int,
    approve: bool,
    comments: Optional[str],
    db: Session
):
    """
    Process approval/rejection and move to next level
    """
    leave_request = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_request_id
    ).first()

    if not leave_request:
        raise HTTPException(status_code=404, detail="Leave request not found")

    # Check for active delegation
    delegate_id = get_active_delegate(approver_id, date.today(), db)
    effective_approver_id = delegate_id if delegate_id else approver_id

    # Find pending workflow for this approver
    workflow = db.query(ApprovalWorkflow).filter(
        ApprovalWorkflow.leave_request_id == leave_request_id,
        ApprovalWorkflow.approver_id == approver_id,
        ApprovalWorkflow.status == ApprovalStatus.PENDING
    ).first()

    if not workflow:
        raise HTTPException(
            status_code=404,
            detail="No pending approval found for this user"
        )

    # Check if this is the current approval level
    previous_levels = db.query(ApprovalWorkflow).filter(
        ApprovalWorkflow.leave_request_id == leave_request_id,
        ApprovalWorkflow.approval_level < workflow.approval_level,
        ApprovalWorkflow.status != ApprovalStatus.APPROVED
    ).all()

    if previous_levels:
        raise HTTPException(
            status_code=400,
            detail="Previous approval levels must be completed first"
        )

    # Update workflow
    workflow.status = ApprovalStatus.APPROVED if approve else ApprovalStatus.REJECTED
    workflow.comments = comments
    workflow.approved_at = datetime.utcnow()

    if not approve:
        # Rejection - update leave request and restore balance
        leave_request.status = RequestStatus.REJECTED
        leave_request.updated_at = datetime.utcnow()

        # Restore pending days to available
        balance = db.query(LeaveBalance).filter(
            LeaveBalance.user_id == leave_request.user_id,
            LeaveBalance.leave_type_id == leave_request.leave_type_id,
            LeaveBalance.year == leave_request.start_date.year
        ).first()

        if balance:
            balance.pending_days -= leave_request.total_days
    else:
        # Check if this is the last approval level
        remaining_approvals = db.query(ApprovalWorkflow).filter(
            ApprovalWorkflow.leave_request_id == leave_request_id,
            ApprovalWorkflow.approval_level > workflow.approval_level
        ).all()

        if not remaining_approvals:
            # Final approval - update leave request and balance
            leave_request.status = RequestStatus.APPROVED
            leave_request.updated_at = datetime.utcnow()

            # Update balance
            balance = db.query(LeaveBalance).filter(
                LeaveBalance.user_id == leave_request.user_id,
                LeaveBalance.leave_type_id == leave_request.leave_type_id,
                LeaveBalance.year == leave_request.start_date.year
            ).first()

            if balance:
                balance.used_days += leave_request.total_days
                balance.pending_days -= leave_request.total_days

    db.commit()
