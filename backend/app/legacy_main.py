"""
FastAPI Employee Leave Management System
A comprehensive HR portal for managing employee leave requests with multi-level approval workflows
"""

from datetime import datetime, timedelta, date
from typing import Optional, List, Annotated
from enum import Enum
import os

from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from jose import JWTError, jwt
import bcrypt as bcrypt_lib

# ============================================================================
# CONFIGURATION
# ============================================================================

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production-min-32-chars")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

DATABASE_URL = "sqlite:///./leave_management.db"

# ============================================================================
# DATABASE SETUP
# ============================================================================

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ============================================================================
# ENUMS
# ============================================================================

class UserRole(str, Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    HR_ADMIN = "hr_admin"

class RequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

# ============================================================================
# DATABASE MODELS
# ============================================================================

class User(Base):
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

    manager = relationship("User", remote_side=[id], backref="team_members")
    leave_balances = relationship("LeaveBalance", back_populates="user")
    leave_requests = relationship("LeaveRequest", back_populates="user")

class LeaveType(Base):
    __tablename__ = "leave_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    annual_quota = Column(Float, nullable=False)
    requires_documentation = Column(Boolean, default=False)
    is_paid = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)

    leave_balances = relationship("LeaveBalance", back_populates="leave_type")
    leave_requests = relationship("LeaveRequest", back_populates="leave_type")

class LeaveBalance(Base):
    __tablename__ = "leave_balances"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    leave_type_id = Column(Integer, ForeignKey("leave_types.id"), nullable=False)
    year = Column(Integer, nullable=False)
    total_days = Column(Float, nullable=False)
    used_days = Column(Float, default=0)
    pending_days = Column(Float, default=0)

    user = relationship("User", back_populates="leave_balances")
    leave_type = relationship("LeaveType", back_populates="leave_balances")

    @property
    def available_days(self) -> float:
        return self.total_days - self.used_days - self.pending_days

class LeaveRequest(Base):
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

    user = relationship("User", back_populates="leave_requests")
    leave_type = relationship("LeaveType", back_populates="leave_requests")
    approval_workflow = relationship("ApprovalWorkflow", back_populates="leave_request")

class ApprovalWorkflow(Base):
    __tablename__ = "approval_workflow"

    id = Column(Integer, primary_key=True, index=True)
    leave_request_id = Column(Integer, ForeignKey("leave_requests.id"), nullable=False)
    approver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    approval_level = Column(Integer, nullable=False)
    status = Column(SQLEnum(ApprovalStatus), default=ApprovalStatus.PENDING)
    comments = Column(String, nullable=True)
    approved_at = Column(DateTime, nullable=True)

    leave_request = relationship("LeaveRequest", back_populates="approval_workflow")
    approver = relationship("User")

class Holiday(Base):
    __tablename__ = "holidays"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    is_mandatory = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    creator = relationship("User")

class Delegation(Base):
    __tablename__ = "delegations"

    id = Column(Integer, primary_key=True, index=True)
    delegator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    delegate_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)

    delegator = relationship("User", foreign_keys=[delegator_id])
    delegate = relationship("User", foreign_keys=[delegate_id])

# ============================================================================
# PYDANTIC SCHEMAS
# ============================================================================

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.EMPLOYEE
    manager_id: Optional[int] = None
    department: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    department: Optional[str] = None
    manager_id: Optional[int] = None

class UserResponse(UserBase):
    id: int
    hire_date: date
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = None

# Leave Type Schemas
class LeaveTypeBase(BaseModel):
    name: str
    annual_quota: float = Field(gt=0)
    requires_documentation: bool = False
    is_paid: bool = True

class LeaveTypeCreate(LeaveTypeBase):
    pass

class LeaveTypeUpdate(BaseModel):
    name: Optional[str] = None
    annual_quota: Optional[float] = Field(default=None, gt=0)
    requires_documentation: Optional[bool] = None
    is_paid: Optional[bool] = None

class LeaveTypeResponse(LeaveTypeBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

# Leave Balance Schemas
class LeaveBalanceResponse(BaseModel):
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
    leave_type_id: int
    start_date: date
    end_date: date
    reason: Optional[str] = None

class LeaveRequestUpdate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    reason: Optional[str] = None

class LeaveRequestResponse(BaseModel):
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
    comments: Optional[str] = None

class ApprovalWorkflowResponse(BaseModel):
    id: int
    leave_request_id: int
    approver_id: int
    approver_name: str
    approval_level: int
    status: ApprovalStatus
    comments: Optional[str]
    approved_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

# Holiday Schemas
class HolidayCreate(BaseModel):
    name: str
    date: date
    is_mandatory: bool = True

class HolidayUpdate(BaseModel):
    name: Optional[str] = None
    date: Optional[date] = None
    is_mandatory: Optional[bool] = None

class HolidayResponse(BaseModel):
    id: int
    name: str
    date: date
    is_mandatory: bool
    created_by: int

    model_config = ConfigDict(from_attributes=True)

# Delegation Schemas
class DelegationCreate(BaseModel):
    delegate_id: int
    start_date: date
    end_date: date

class DelegationResponse(BaseModel):
    id: int
    delegator_id: int
    delegator_name: str
    delegate_id: int
    delegate_name: str
    start_date: date
    end_date: date
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

# ============================================================================
# AUTHENTICATION UTILITIES
# ============================================================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_lib.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    salt = bcrypt_lib.gensalt()
    hashed = bcrypt_lib.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        email: str = payload.get("email")
        role: str = payload.get("role")
        if user_id is None or email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return TokenData(user_id=user_id, email=email, role=role)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# ============================================================================
# DATABASE UTILITIES
# ============================================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)) -> User:
    token_data = decode_access_token(token)
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")
    return user

def require_role(allowed_roles: List[UserRole]):
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join([r.value for r in allowed_roles])}"
            )
        return current_user
    return role_checker

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def calculate_working_days(start_date: date, end_date: date, db: Session) -> float:
    """Calculate working days excluding weekends and holidays"""
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

def check_overlapping_requests(user_id: int, start_date: date, end_date: date, db: Session, exclude_request_id: Optional[int] = None) -> bool:
    """Check if user has overlapping leave requests"""
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
    """Get active delegate for an approver on a specific date"""
    delegation = db.query(Delegation).filter(
        Delegation.delegator_id == approver_id,
        Delegation.is_active == True,
        Delegation.start_date <= approval_date,
        Delegation.end_date >= approval_date
    ).first()

    return delegation.delegate_id if delegation else None

# ============================================================================
# WORKFLOW ENGINE
# ============================================================================

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
        hr_admin = db.query(User).filter(User.role == UserRole.HR_ADMIN, User.is_active == True).first()
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
            hr_admin = db.query(User).filter(User.role == UserRole.HR_ADMIN, User.is_active == True).first()
            if hr_admin:
                workflow = ApprovalWorkflow(
                    leave_request_id=leave_request.id,
                    approver_id=hr_admin.id,
                    approval_level=approval_level,
                    status=ApprovalStatus.PENDING
                )
                db.add(workflow)

    db.commit()

def process_approval(leave_request_id: int, approver_id: int, approve: bool, comments: Optional[str], db: Session):
    """Process approval/rejection and move to next level"""
    leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == leave_request_id).first()
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
        raise HTTPException(status_code=404, detail="No pending approval found for this user")

    # Check if this is the current approval level
    previous_levels = db.query(ApprovalWorkflow).filter(
        ApprovalWorkflow.leave_request_id == leave_request_id,
        ApprovalWorkflow.approval_level < workflow.approval_level,
        ApprovalWorkflow.status != ApprovalStatus.APPROVED
    ).all()

    if previous_levels:
        raise HTTPException(status_code=400, detail="Previous approval levels must be completed first")

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

# ============================================================================
# API ROUTERS
# ============================================================================

# Authentication Router
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/register", response_model=UserResponse)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.HR_ADMIN]))
):
    """Register a new user (HR Admin only)"""
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        password_hash=get_password_hash(user_data.password),
        role=user_data.role,
        manager_id=user_data.manager_id,
        department=user_data.department,
        hire_date=date.today()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@auth_router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login and get JWT token"""
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(status_code=400, detail="User account is inactive")

    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email, "role": user.role.value}
    )

    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return current_user

# Users Router
users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.get("", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.MANAGER, UserRole.HR_ADMIN]))
):
    """List all users (Manager/HR Admin only)"""
    if current_user.role == UserRole.MANAGER:
        # Managers can only see their team
        users = db.query(User).filter(User.manager_id == current_user.id).all()
    else:
        # HR Admins can see all users
        users = db.query(User).filter(User.is_active == True).all()

    return users

@users_router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user details"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Authorization check
    if current_user.role == UserRole.EMPLOYEE and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    return user

@users_router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user profile"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Authorization: users can update their own profile, HR admins can update anyone
    if current_user.role != UserRole.HR_ADMIN and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Update fields
    if user_data.full_name is not None:
        user.full_name = user_data.full_name
    if user_data.department is not None:
        user.department = user_data.department
    if user_data.manager_id is not None and current_user.role == UserRole.HR_ADMIN:
        user.manager_id = user_data.manager_id

    db.commit()
    db.refresh(user)
    return user

@users_router.get("/{user_id}/team", response_model=List[UserResponse])
def get_team_members(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.MANAGER, UserRole.HR_ADMIN]))
):
    """Get team members for a manager"""
    # Authorization check
    if current_user.role == UserRole.MANAGER and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    team_members = db.query(User).filter(User.manager_id == user_id, User.is_active == True).all()
    return team_members

# Leave Types Router
leave_types_router = APIRouter(prefix="/leave-types", tags=["Leave Types"])

@leave_types_router.get("", response_model=List[LeaveTypeResponse])
def list_leave_types(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """List all active leave types"""
    leave_types = db.query(LeaveType).filter(LeaveType.is_active == True).all()
    return leave_types

@leave_types_router.post("", response_model=LeaveTypeResponse)
def create_leave_type(
    leave_type_data: LeaveTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.HR_ADMIN]))
):
    """Create a new leave type (HR Admin only)"""
    # Check if leave type already exists
    existing = db.query(LeaveType).filter(LeaveType.name == leave_type_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Leave type already exists")

    leave_type = LeaveType(**leave_type_data.model_dump())
    db.add(leave_type)
    db.commit()
    db.refresh(leave_type)
    return leave_type

@leave_types_router.put("/{leave_type_id}", response_model=LeaveTypeResponse)
def update_leave_type(
    leave_type_id: int,
    leave_type_data: LeaveTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.HR_ADMIN]))
):
    """Update a leave type (HR Admin only)"""
    leave_type = db.query(LeaveType).filter(LeaveType.id == leave_type_id).first()
    if not leave_type:
        raise HTTPException(status_code=404, detail="Leave type not found")

    # Update fields
    update_data = leave_type_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(leave_type, field, value)

    db.commit()
    db.refresh(leave_type)
    return leave_type

@leave_types_router.delete("/{leave_type_id}")
def deactivate_leave_type(
    leave_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.HR_ADMIN]))
):
    """Deactivate a leave type (HR Admin only)"""
    leave_type = db.query(LeaveType).filter(LeaveType.id == leave_type_id).first()
    if not leave_type:
        raise HTTPException(status_code=404, detail="Leave type not found")

    leave_type.is_active = False
    db.commit()
    return {"message": "Leave type deactivated successfully"}

# Leave Balances Router
leave_balances_router = APIRouter(prefix="/leave-balances", tags=["Leave Balances"])

@leave_balances_router.get("/me", response_model=List[LeaveBalanceResponse])
def get_my_leave_balances(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's leave balances"""
    current_year = date.today().year
    balances = db.query(LeaveBalance).filter(
        LeaveBalance.user_id == current_user.id,
        LeaveBalance.year == current_year
    ).all()

    result = []
    for balance in balances:
        result.append(LeaveBalanceResponse(
            id=balance.id,
            user_id=balance.user_id,
            leave_type_id=balance.leave_type_id,
            leave_type_name=balance.leave_type.name,
            year=balance.year,
            total_days=balance.total_days,
            used_days=balance.used_days,
            pending_days=balance.pending_days,
            available_days=balance.available_days
        ))

    return result

@leave_balances_router.get("/{user_id}", response_model=List[LeaveBalanceResponse])
def get_user_leave_balances(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.MANAGER, UserRole.HR_ADMIN]))
):
    """Get user's leave balances (Manager/HR Admin only)"""
    current_year = date.today().year
    balances = db.query(LeaveBalance).filter(
        LeaveBalance.user_id == user_id,
        LeaveBalance.year == current_year
    ).all()

    result = []
    for balance in balances:
        result.append(LeaveBalanceResponse(
            id=balance.id,
            user_id=balance.user_id,
            leave_type_id=balance.leave_type_id,
            leave_type_name=balance.leave_type.name,
            year=balance.year,
            total_days=balance.total_days,
            used_days=balance.used_days,
            pending_days=balance.pending_days,
            available_days=balance.available_days
        ))

    return result

@leave_balances_router.post("/initialize/{year}")
def initialize_leave_balances(
    year: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.HR_ADMIN]))
):
    """Initialize leave balances for all users for a given year (HR Admin only)"""
    # Get all active users and leave types
    users = db.query(User).filter(User.is_active == True).all()
    leave_types = db.query(LeaveType).filter(LeaveType.is_active == True).all()

    initialized_count = 0
    for user in users:
        for leave_type in leave_types:
            # Check if balance already exists
            existing = db.query(LeaveBalance).filter(
                LeaveBalance.user_id == user.id,
                LeaveBalance.leave_type_id == leave_type.id,
                LeaveBalance.year == year
            ).first()

            if not existing:
                balance = LeaveBalance(
                    user_id=user.id,
                    leave_type_id=leave_type.id,
                    year=year,
                    total_days=leave_type.annual_quota,
                    used_days=0,
                    pending_days=0
                )
                db.add(balance)
                initialized_count += 1

    db.commit()
    return {"message": f"Initialized {initialized_count} leave balances for year {year}"}

# Leave Requests Router
leave_requests_router = APIRouter(prefix="/leave-requests", tags=["Leave Requests"])

@leave_requests_router.post("", response_model=LeaveRequestResponse)
def create_leave_request(
    request_data: LeaveRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit a new leave request"""
    # Validate dates
    if request_data.start_date > request_data.end_date:
        raise HTTPException(status_code=400, detail="Start date must be before end date")

    if request_data.start_date < date.today():
        raise HTTPException(status_code=400, detail="Cannot request leave for past dates")

    # Calculate working days
    total_days = calculate_working_days(request_data.start_date, request_data.end_date, db)

    if total_days == 0:
        raise HTTPException(status_code=400, detail="Leave request must include at least one working day")

    # Check for overlapping requests
    if check_overlapping_requests(current_user.id, request_data.start_date, request_data.end_date, db):
        raise HTTPException(status_code=400, detail="You have an overlapping leave request")

    # Check leave balance
    current_year = request_data.start_date.year
    balance = db.query(LeaveBalance).filter(
        LeaveBalance.user_id == current_user.id,
        LeaveBalance.leave_type_id == request_data.leave_type_id,
        LeaveBalance.year == current_year
    ).first()

    if not balance:
        raise HTTPException(status_code=400, detail="Leave balance not found for this year")

    if balance.available_days < total_days:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient leave balance. Available: {balance.available_days}, Requested: {total_days}"
        )

    # Create leave request
    leave_request = LeaveRequest(
        user_id=current_user.id,
        leave_type_id=request_data.leave_type_id,
        start_date=request_data.start_date,
        end_date=request_data.end_date,
        total_days=total_days,
        reason=request_data.reason,
        status=RequestStatus.PENDING
    )
    db.add(leave_request)
    db.commit()
    db.refresh(leave_request)

    # Update pending days in balance
    balance.pending_days += total_days

    # Create approval workflow
    create_approval_workflow(leave_request, db)

    db.commit()

    return LeaveRequestResponse(
        id=leave_request.id,
        user_id=leave_request.user_id,
        user_name=leave_request.user.full_name,
        leave_type_id=leave_request.leave_type_id,
        leave_type_name=leave_request.leave_type.name,
        start_date=leave_request.start_date,
        end_date=leave_request.end_date,
        total_days=leave_request.total_days,
        reason=leave_request.reason,
        status=leave_request.status,
        created_at=leave_request.created_at,
        updated_at=leave_request.updated_at
    )

@leave_requests_router.get("", response_model=List[LeaveRequestResponse])
def list_leave_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List leave requests (filtered by role)"""
    if current_user.role == UserRole.HR_ADMIN:
        # HR can see all requests
        requests = db.query(LeaveRequest).order_by(LeaveRequest.created_at.desc()).all()
    elif current_user.role == UserRole.MANAGER:
        # Managers can see their team's requests
        team_member_ids = [tm.id for tm in current_user.team_members]
        team_member_ids.append(current_user.id)  # Include own requests
        requests = db.query(LeaveRequest).filter(
            LeaveRequest.user_id.in_(team_member_ids)
        ).order_by(LeaveRequest.created_at.desc()).all()
    else:
        # Employees can only see their own requests
        requests = db.query(LeaveRequest).filter(
            LeaveRequest.user_id == current_user.id
        ).order_by(LeaveRequest.created_at.desc()).all()

    result = []
    for req in requests:
        result.append(LeaveRequestResponse(
            id=req.id,
            user_id=req.user_id,
            user_name=req.user.full_name,
            leave_type_id=req.leave_type_id,
            leave_type_name=req.leave_type.name,
            start_date=req.start_date,
            end_date=req.end_date,
            total_days=req.total_days,
            reason=req.reason,
            status=req.status,
            created_at=req.created_at,
            updated_at=req.updated_at
        ))

    return result

@leave_requests_router.get("/pending-approvals", response_model=List[LeaveRequestResponse])
def get_pending_approvals(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.MANAGER, UserRole.HR_ADMIN]))
):
    """Get leave requests awaiting my approval"""
    # Find pending approvals for current user
    pending_workflows = db.query(ApprovalWorkflow).filter(
        ApprovalWorkflow.approver_id == current_user.id,
        ApprovalWorkflow.status == ApprovalStatus.PENDING
    ).all()

    result = []
    for workflow in pending_workflows:
        req = workflow.leave_request
        if req.status == RequestStatus.PENDING:
            result.append(LeaveRequestResponse(
                id=req.id,
                user_id=req.user_id,
                user_name=req.user.full_name,
                leave_type_id=req.leave_type_id,
                leave_type_name=req.leave_type.name,
                start_date=req.start_date,
                end_date=req.end_date,
                total_days=req.total_days,
                reason=req.reason,
                status=req.status,
                created_at=req.created_at,
                updated_at=req.updated_at
            ))

    return result

@leave_requests_router.get("/{request_id}", response_model=LeaveRequestResponse)
def get_leave_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get leave request details"""
    leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == request_id).first()
    if not leave_request:
        raise HTTPException(status_code=404, detail="Leave request not found")

    # Authorization check
    if current_user.role == UserRole.EMPLOYEE and leave_request.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return LeaveRequestResponse(
        id=leave_request.id,
        user_id=leave_request.user_id,
        user_name=leave_request.user.full_name,
        leave_type_id=leave_request.leave_type_id,
        leave_type_name=leave_request.leave_type.name,
        start_date=leave_request.start_date,
        end_date=leave_request.end_date,
        total_days=leave_request.total_days,
        reason=leave_request.reason,
        status=leave_request.status,
        created_at=leave_request.created_at,
        updated_at=leave_request.updated_at
    )

@leave_requests_router.put("/{request_id}", response_model=LeaveRequestResponse)
def update_leave_request(
    request_id: int,
    request_data: LeaveRequestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update leave request (only before approval)"""
    leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == request_id).first()
    if not leave_request:
        raise HTTPException(status_code=404, detail="Leave request not found")

    # Authorization check
    if leave_request.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Can only update pending requests
    if leave_request.status != RequestStatus.PENDING:
        raise HTTPException(status_code=400, detail="Cannot update non-pending requests")

    # Update fields
    if request_data.start_date or request_data.end_date:
        start_date = request_data.start_date or leave_request.start_date
        end_date = request_data.end_date or leave_request.end_date

        if start_date > end_date:
            raise HTTPException(status_code=400, detail="Start date must be before end date")

        # Recalculate working days
        new_total_days = calculate_working_days(start_date, end_date, db)

        # Check for overlapping requests
        if check_overlapping_requests(current_user.id, start_date, end_date, db, exclude_request_id=request_id):
            raise HTTPException(status_code=400, detail="Updated dates overlap with another leave request")

        # Update balance
        balance = db.query(LeaveBalance).filter(
            LeaveBalance.user_id == current_user.id,
            LeaveBalance.leave_type_id == leave_request.leave_type_id,
            LeaveBalance.year == start_date.year
        ).first()

        if balance:
            # Restore old pending days and add new
            balance.pending_days -= leave_request.total_days

            if balance.available_days < new_total_days:
                raise HTTPException(status_code=400, detail="Insufficient leave balance for updated dates")

            balance.pending_days += new_total_days

        leave_request.start_date = start_date
        leave_request.end_date = end_date
        leave_request.total_days = new_total_days

    if request_data.reason is not None:
        leave_request.reason = request_data.reason

    leave_request.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(leave_request)

    return LeaveRequestResponse(
        id=leave_request.id,
        user_id=leave_request.user_id,
        user_name=leave_request.user.full_name,
        leave_type_id=leave_request.leave_type_id,
        leave_type_name=leave_request.leave_type.name,
        start_date=leave_request.start_date,
        end_date=leave_request.end_date,
        total_days=leave_request.total_days,
        reason=leave_request.reason,
        status=leave_request.status,
        created_at=leave_request.created_at,
        updated_at=leave_request.updated_at
    )

@leave_requests_router.delete("/{request_id}")
def cancel_leave_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cancel leave request"""
    leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == request_id).first()
    if not leave_request:
        raise HTTPException(status_code=404, detail="Leave request not found")

    # Authorization check
    if leave_request.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Can only cancel pending or approved requests (not past dates)
    if leave_request.status not in [RequestStatus.PENDING, RequestStatus.APPROVED]:
        raise HTTPException(status_code=400, detail="Cannot cancel this request")

    if leave_request.start_date < date.today():
        raise HTTPException(status_code=400, detail="Cannot cancel past leave requests")

    # Update status
    old_status = leave_request.status
    leave_request.status = RequestStatus.CANCELLED
    leave_request.updated_at = datetime.utcnow()

    # Restore balance
    balance = db.query(LeaveBalance).filter(
        LeaveBalance.user_id == leave_request.user_id,
        LeaveBalance.leave_type_id == leave_request.leave_type_id,
        LeaveBalance.year == leave_request.start_date.year
    ).first()

    if balance:
        if old_status == RequestStatus.PENDING:
            balance.pending_days -= leave_request.total_days
        elif old_status == RequestStatus.APPROVED:
            balance.used_days -= leave_request.total_days

    db.commit()
    return {"message": "Leave request cancelled successfully"}

# Approvals Router
approvals_router = APIRouter(prefix="/approvals", tags=["Approvals"])

@approvals_router.post("/{request_id}/approve")
def approve_leave_request(
    request_id: int,
    approval_data: ApprovalAction,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.MANAGER, UserRole.HR_ADMIN]))
):
    """Approve leave request"""
    process_approval(request_id, current_user.id, True, approval_data.comments, db)
    return {"message": "Leave request approved successfully"}

@approvals_router.post("/{request_id}/reject")
def reject_leave_request(
    request_id: int,
    approval_data: ApprovalAction,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.MANAGER, UserRole.HR_ADMIN]))
):
    """Reject leave request"""
    process_approval(request_id, current_user.id, False, approval_data.comments, db)
    return {"message": "Leave request rejected successfully"}

@approvals_router.get("/my-pending", response_model=List[ApprovalWorkflowResponse])
def get_my_pending_approvals(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.MANAGER, UserRole.HR_ADMIN]))
):
    """Get my pending approval tasks"""
    workflows = db.query(ApprovalWorkflow).filter(
        ApprovalWorkflow.approver_id == current_user.id,
        ApprovalWorkflow.status == ApprovalStatus.PENDING
    ).all()

    result = []
    for workflow in workflows:
        result.append(ApprovalWorkflowResponse(
            id=workflow.id,
            leave_request_id=workflow.leave_request_id,
            approver_id=workflow.approver_id,
            approver_name=workflow.approver.full_name,
            approval_level=workflow.approval_level,
            status=workflow.status,
            comments=workflow.comments,
            approved_at=workflow.approved_at
        ))

    return result

# Holidays Router
holidays_router = APIRouter(prefix="/holidays", tags=["Holidays"])

@holidays_router.get("", response_model=List[HolidayResponse])
def list_holidays(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """List all holidays"""
    holidays = db.query(Holiday).order_by(Holiday.date).all()
    return holidays

@holidays_router.post("", response_model=HolidayResponse)
def create_holiday(
    holiday_data: HolidayCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.HR_ADMIN]))
):
    """Create a new holiday (HR Admin only)"""
    holiday = Holiday(
        name=holiday_data.name,
        date=holiday_data.date,
        is_mandatory=holiday_data.is_mandatory,
        created_by=current_user.id
    )
    db.add(holiday)
    db.commit()
    db.refresh(holiday)
    return holiday

@holidays_router.put("/{holiday_id}", response_model=HolidayResponse)
def update_holiday(
    holiday_id: int,
    holiday_data: HolidayUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.HR_ADMIN]))
):
    """Update a holiday (HR Admin only)"""
    holiday = db.query(Holiday).filter(Holiday.id == holiday_id).first()
    if not holiday:
        raise HTTPException(status_code=404, detail="Holiday not found")

    update_data = holiday_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(holiday, field, value)

    db.commit()
    db.refresh(holiday)
    return holiday

@holidays_router.delete("/{holiday_id}")
def delete_holiday(
    holiday_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.HR_ADMIN]))
):
    """Delete a holiday (HR Admin only)"""
    holiday = db.query(Holiday).filter(Holiday.id == holiday_id).first()
    if not holiday:
        raise HTTPException(status_code=404, detail="Holiday not found")

    db.delete(holiday)
    db.commit()
    return {"message": "Holiday deleted successfully"}

@holidays_router.get("/{year}", response_model=List[HolidayResponse])
def get_holidays_by_year(
    year: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get holidays for a specific year"""
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)

    holidays = db.query(Holiday).filter(
        Holiday.date >= start_date,
        Holiday.date <= end_date
    ).order_by(Holiday.date).all()

    return holidays

# Delegations Router
delegations_router = APIRouter(prefix="/delegations", tags=["Delegations"])

@delegations_router.post("", response_model=DelegationResponse)
def create_delegation(
    delegation_data: DelegationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.MANAGER, UserRole.HR_ADMIN]))
):
    """Create a delegation"""
    # Validate dates
    if delegation_data.start_date > delegation_data.end_date:
        raise HTTPException(status_code=400, detail="Start date must be before end date")

    # Validate delegate exists
    delegate = db.query(User).filter(User.id == delegation_data.delegate_id).first()
    if not delegate:
        raise HTTPException(status_code=404, detail="Delegate user not found")

    # Create delegation
    delegation = Delegation(
        delegator_id=current_user.id,
        delegate_id=delegation_data.delegate_id,
        start_date=delegation_data.start_date,
        end_date=delegation_data.end_date,
        is_active=True
    )
    db.add(delegation)
    db.commit()
    db.refresh(delegation)

    return DelegationResponse(
        id=delegation.id,
        delegator_id=delegation.delegator_id,
        delegator_name=delegation.delegator.full_name,
        delegate_id=delegation.delegate_id,
        delegate_name=delegation.delegate.full_name,
        start_date=delegation.start_date,
        end_date=delegation.end_date,
        is_active=delegation.is_active
    )

@delegations_router.get("/active", response_model=List[DelegationResponse])
def get_active_delegations(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.MANAGER, UserRole.HR_ADMIN]))
):
    """Get active delegations"""
    today = date.today()

    # Get delegations where current user is delegator or delegate
    delegations = db.query(Delegation).filter(
        Delegation.is_active == True,
        Delegation.start_date <= today,
        Delegation.end_date >= today,
        (Delegation.delegator_id == current_user.id) | (Delegation.delegate_id == current_user.id)
    ).all()

    result = []
    for delegation in delegations:
        result.append(DelegationResponse(
            id=delegation.id,
            delegator_id=delegation.delegator_id,
            delegator_name=delegation.delegator.full_name,
            delegate_id=delegation.delegate_id,
            delegate_name=delegation.delegate.full_name,
            start_date=delegation.start_date,
            end_date=delegation.end_date,
            is_active=delegation.is_active
        ))

    return result

@delegations_router.delete("/{delegation_id}")
def cancel_delegation(
    delegation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.MANAGER, UserRole.HR_ADMIN]))
):
    """Cancel a delegation"""
    delegation = db.query(Delegation).filter(Delegation.id == delegation_id).first()
    if not delegation:
        raise HTTPException(status_code=404, detail="Delegation not found")

    # Authorization check
    if delegation.delegator_id != current_user.id and current_user.role != UserRole.HR_ADMIN:
        raise HTTPException(status_code=403, detail="Access denied")

    delegation.is_active = False
    db.commit()
    return {"message": "Delegation cancelled successfully"}

# Reports Router
reports_router = APIRouter(prefix="/reports", tags=["Reports"])

@reports_router.get("/team-calendar")
def get_team_calendar(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.MANAGER, UserRole.HR_ADMIN]))
):
    """Get team leave calendar view"""
    if current_user.role == UserRole.MANAGER:
        team_member_ids = [tm.id for tm in current_user.team_members]
        team_member_ids.append(current_user.id)
    else:
        # HR can see all
        team_member_ids = [u.id for u in db.query(User).filter(User.is_active == True).all()]

    leave_requests = db.query(LeaveRequest).filter(
        LeaveRequest.user_id.in_(team_member_ids),
        LeaveRequest.status == RequestStatus.APPROVED,
        LeaveRequest.start_date <= end_date,
        LeaveRequest.end_date >= start_date
    ).all()

    calendar = []
    for req in leave_requests:
        calendar.append({
            "user_id": req.user_id,
            "user_name": req.user.full_name,
            "leave_type": req.leave_type.name,
            "start_date": req.start_date,
            "end_date": req.end_date,
            "total_days": req.total_days
        })

    return {"calendar": calendar}

@reports_router.get("/leave-summary")
def get_leave_summary(
    year: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.HR_ADMIN]))
):
    """Get leave usage summary by department (HR Admin only)"""
    users = db.query(User).filter(User.is_active == True).all()

    summary = {}
    for user in users:
        dept = user.department or "Unassigned"
        if dept not in summary:
            summary[dept] = {
                "total_employees": 0,
                "total_used_days": 0,
                "total_pending_days": 0
            }

        summary[dept]["total_employees"] += 1

        balances = db.query(LeaveBalance).filter(
            LeaveBalance.user_id == user.id,
            LeaveBalance.year == year
        ).all()

        for balance in balances:
            summary[dept]["total_used_days"] += balance.used_days
            summary[dept]["total_pending_days"] += balance.pending_days

    return {"year": year, "summary": summary}

@reports_router.get("/pending-requests")
def get_all_pending_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.HR_ADMIN]))
):
    """Get all pending leave requests (HR Admin only)"""
    requests = db.query(LeaveRequest).filter(
        LeaveRequest.status == RequestStatus.PENDING
    ).order_by(LeaveRequest.created_at).all()

    result = []
    for req in requests:
        # Get approval workflow
        workflows = db.query(ApprovalWorkflow).filter(
            ApprovalWorkflow.leave_request_id == req.id
        ).order_by(ApprovalWorkflow.approval_level).all()

        result.append({
            "request_id": req.id,
            "user_name": req.user.full_name,
            "leave_type": req.leave_type.name,
            "start_date": req.start_date,
            "end_date": req.end_date,
            "total_days": req.total_days,
            "created_at": req.created_at,
            "approval_workflow": [
                {
                    "level": w.approval_level,
                    "approver": w.approver.full_name,
                    "status": w.status.value
                }
                for w in workflows
            ]
        })

    return {"pending_requests": result}

@reports_router.get("/user-leave-history/{user_id}")
def get_user_leave_history(
    user_id: int,
    year: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.MANAGER, UserRole.HR_ADMIN]))
):
    """Get user's leave history"""
    if not year:
        year = date.today().year

    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)

    requests = db.query(LeaveRequest).filter(
        LeaveRequest.user_id == user_id,
        LeaveRequest.start_date >= start_date,
        LeaveRequest.end_date <= end_date
    ).order_by(LeaveRequest.start_date).all()

    history = []
    for req in requests:
        history.append({
            "request_id": req.id,
            "leave_type": req.leave_type.name,
            "start_date": req.start_date,
            "end_date": req.end_date,
            "total_days": req.total_days,
            "status": req.status.value,
            "reason": req.reason
        })

    return {"user_id": user_id, "year": year, "history": history}

# ============================================================================
# SEED DATA
# ============================================================================

def seed_data(db: Session):
    """Initialize database with default data"""
    # Check if data already exists
    existing_user = db.query(User).first()
    if existing_user:
        return

    print("Seeding database with initial data...")

    # Create default HR admin
    hr_admin = User(
        email="admin@company.com",
        full_name="HR Administrator",
        password_hash=get_password_hash("admin123"),
        role=UserRole.HR_ADMIN,
        department="Human Resources",
        hire_date=date(2020, 1, 1)
    )
    db.add(hr_admin)
    db.commit()
    db.refresh(hr_admin)

    # Create sample manager
    manager = User(
        email="manager@company.com",
        full_name="John Manager",
        password_hash=get_password_hash("manager123"),
        role=UserRole.MANAGER,
        department="Engineering",
        hire_date=date(2021, 1, 1)
    )
    db.add(manager)
    db.commit()
    db.refresh(manager)

    # Create sample employee
    employee = User(
        email="employee@company.com",
        full_name="Jane Employee",
        password_hash=get_password_hash("employee123"),
        role=UserRole.EMPLOYEE,
        manager_id=manager.id,
        department="Engineering",
        hire_date=date(2022, 6, 1)
    )
    db.add(employee)

    # Create default leave types
    leave_types_data = [
        {"name": "Annual Leave", "annual_quota": 20, "requires_documentation": False, "is_paid": True},
        {"name": "Sick Leave", "annual_quota": 10, "requires_documentation": True, "is_paid": True},
        {"name": "Personal Leave", "annual_quota": 5, "requires_documentation": False, "is_paid": True},
        {"name": "Bereavement Leave", "annual_quota": 3, "requires_documentation": True, "is_paid": True},
        {"name": "Unpaid Leave", "annual_quota": 30, "requires_documentation": False, "is_paid": False},
    ]

    leave_types = []
    for lt_data in leave_types_data:
        leave_type = LeaveType(**lt_data)
        db.add(leave_type)
        leave_types.append(leave_type)

    db.commit()

    # Initialize leave balances for current year
    current_year = date.today().year
    users = [hr_admin, manager, employee]

    for user in users:
        for leave_type in leave_types:
            balance = LeaveBalance(
                user_id=user.id,
                leave_type_id=leave_type.id,
                year=current_year,
                total_days=leave_type.annual_quota,
                used_days=0,
                pending_days=0
            )
            db.add(balance)

    # Add some sample holidays
    holidays_data = [
        {"name": "New Year's Day", "date": date(current_year, 1, 1)},
        {"name": "Independence Day", "date": date(current_year, 7, 4)},
        {"name": "Thanksgiving", "date": date(current_year, 11, 28)},
        {"name": "Christmas", "date": date(current_year, 12, 25)},
    ]

    for holiday_data in holidays_data:
        holiday = Holiday(
            name=holiday_data["name"],
            date=holiday_data["date"],
            is_mandatory=True,
            created_by=hr_admin.id
        )
        db.add(holiday)

    db.commit()
    print("Database seeded successfully!")
    print("\nDefault credentials:")
    print("  HR Admin    - Email: admin@company.com    | Password: admin123")
    print("  Manager     - Email: manager@company.com  | Password: manager123")
    print("  Employee    - Email: employee@company.com | Password: employee123")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

app = FastAPI(
    title="HR Leave Management System",
    description="Enterprise HR portal for employee leave management with multi-level approval workflows",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(leave_types_router)
app.include_router(leave_balances_router)
app.include_router(leave_requests_router)
app.include_router(approvals_router)
app.include_router(holidays_router)
app.include_router(delegations_router)
app.include_router(reports_router)

@app.on_event("startup")
def startup_event():
    """Initialize database and seed data on startup"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "HR Leave Management System API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "status": "active"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*70)
    print("HR LEAVE MANAGEMENT SYSTEM")
    print("="*70)
    print("\nStarting server...")
    print("API Documentation: http://localhost:8001/docs")
    print("Alternative Docs:  http://localhost:8001/redoc")
    print("\n" + "="*70 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
