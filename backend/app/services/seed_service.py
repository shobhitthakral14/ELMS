"""
Database seeding service
"""
from datetime import date
from sqlalchemy.orm import Session
from ..models import User, LeaveType, LeaveBalance, Holiday
from ..schemas import UserRole
from ..utils.auth import get_password_hash


def seed_database(db: Session):
    """
    Initialize database with default data
    """
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
