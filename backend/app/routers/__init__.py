"""
API routers
"""
from .auth import router as auth_router
from .users import router as users_router
from .leave_types import router as leave_types_router
from .leave_balances import router as leave_balances_router
from .leave_requests import router as leave_requests_router
from .approvals import router as approvals_router
from .holidays import router as holidays_router
from .delegations import router as delegations_router
from .reports import router as reports_router

__all__ = [
    "auth_router",
    "users_router",
    "leave_types_router",
    "leave_balances_router",
    "leave_requests_router",
    "approvals_router",
    "holidays_router",
    "delegations_router",
    "reports_router",
]
