"""
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import CORS_ORIGINS
from .database import engine, Base, SessionLocal
from .routers import (
    auth_router,
    users_router,
    leave_types_router,
    leave_balances_router,
    leave_requests_router,
    approvals_router,
    holidays_router,
    delegations_router,
    reports_router
)
from .services import seed_database


# Create FastAPI app
app = FastAPI(
    title="HR Leave Management System",
    description="Enterprise HR portal for employee leave management with multi-level approval workflows",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
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
        seed_database(db)
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
    from datetime import datetime
    return {"status": "healthy", "timestamp": datetime.utcnow()}
