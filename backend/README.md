# Backend - HR Leave Management System

FastAPI backend for employee leave management with multi-level approval workflows.

## 📁 Project Structure

```
backend/
├── app/                          # Main application package
│   ├── __init__.py              # Package initialization
│   ├── config.py                # Configuration settings
│   ├── database.py              # Database setup and session management
│   ├── main.py                  # FastAPI app initialization (modular version)
│   ├── legacy_main.py           # Current working implementation
│   │
│   ├── models/                  # SQLAlchemy database models
│   │   ├── __init__.py         # Export all models
│   │   ├── user.py             # User model
│   │   ├── leave.py            # Leave-related models
│   │   ├── holiday.py          # Holiday model
│   │   └── delegation.py       # Delegation model
│   │
│   ├── schemas/                 # Pydantic schemas for validation
│   │   ├── __init__.py         # Export all schemas
│   │   ├── enums.py            # Enum definitions
│   │   ├── user.py             # User schemas
│   │   ├── leave.py            # Leave schemas
│   │   ├── holiday.py          # Holiday schemas
│   │   └── delegation.py       # Delegation schemas
│   │
│   ├── routers/                 # API route handlers
│   │   ├── __init__.py         # Export all routers
│   │   ├── auth.py             # Authentication endpoints
│   │   ├── users.py            # User management endpoints
│   │   ├── leave_types.py      # Leave types endpoints
│   │   ├── leave_balances.py   # Leave balances endpoints
│   │   ├── leave_requests.py   # Leave requests endpoints
│   │   ├── approvals.py        # Approval endpoints
│   │   ├── holidays.py         # Holiday endpoints
│   │   ├── delegations.py      # Delegation endpoints
│   │   └── reports.py          # Reporting endpoints
│   │
│   ├── services/                # Business logic layer
│   │   ├── __init__.py         # Export all services
│   │   ├── auth_service.py     # Authentication logic
│   │   ├── leave_service.py    # Leave workflow logic
│   │   └── seed_service.py     # Database seeding
│   │
│   └── utils/                   # Utility functions
│       ├── __init__.py         # Export utilities
│       ├── auth.py             # Auth utilities (JWT, password hashing)
│       └── helpers.py          # Helper functions
│
├── leave_management.db          # SQLite database (auto-created)
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
└── README.md                    # This file
```

## 🚀 Quick Start

### Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Run the Server
```bash
python run.py
```

The server will start on http://localhost:8001

## 📚 Architecture Layers

### 1. **Models** (`app/models/`)
SQLAlchemy ORM models representing database tables:
- `User`: Employee information and roles
- `LeaveType`: Different types of leaves
- `LeaveBalance`: Per-user leave balances
- `LeaveRequest`: Leave requests submitted
- `ApprovalWorkflow`: Multi-level approval chain
- `Holiday`: Company holidays
- `Delegation`: Approval authority delegation

### 2. **Schemas** (`app/schemas/`)
Pydantic models for request/response validation:
- Input validation
- Output serialization
- Type safety
- API documentation

### 3. **Routers** (`app/routers/`)
API endpoint handlers organized by feature:
- **Auth**: Login, token management
- **Users**: User CRUD operations
- **Leave Types**: Leave category management
- **Leave Balances**: Balance tracking
- **Leave Requests**: Request submission and management
- **Approvals**: Approval workflow handling
- **Holidays**: Holiday calendar
- **Delegations**: Delegation management
- **Reports**: Analytics and reporting

### 4. **Services** (`app/services/`)
Business logic and workflows:
- Authentication and authorization
- Multi-level approval workflows
- Database seeding
- Complex business rules

### 5. **Utils** (`app/utils/`)
Reusable utility functions:
- JWT token creation/validation
- Password hashing (bcrypt)
- Working days calculation
- Helper functions

## 🔧 Configuration

Edit `app/config.py` to change:
- Database URL
- JWT secret key
- Token expiration time
- CORS origins
- Server host and port

## 🗄️ Database

**Type**: SQLite
**File**: `leave_management.db`
**Auto-created**: Yes (on first run)
**Seeded**: Yes (with default users and data)

### Default Users
- **HR Admin**: admin@company.com / admin123
- **Manager**: manager@company.com / manager123
- **Employee**: employee@company.com / employee123

## 📡 API Endpoints

### Authentication
- `POST /auth/login` - Login
- `POST /auth/register` - Register new user (HR only)
- `GET /auth/me` - Get current user

### Leave Management
- `GET /leave-types` - List leave types
- `GET /leave-balances/me` - My balances
- `POST /leave-requests` - Submit request
- `GET /leave-requests` - List requests
- `DELETE /leave-requests/{id}` - Cancel request

### Approvals
- `GET /leave-requests/pending-approvals` - Pending for me
- `POST /approvals/{id}/approve` - Approve
- `POST /approvals/{id}/reject` - Reject

### Reports (HR Admin)
- `GET /reports/team-calendar` - Team calendar
- `GET /reports/leave-summary` - Usage summary
- `GET /reports/pending-requests` - All pending

## 🔒 Security Features

- **JWT Authentication**: Secure token-based auth
- **Password Hashing**: Bcrypt for passwords
- **Role-Based Access**: Employee/Manager/HR Admin
- **SQL Injection Prevention**: SQLAlchemy ORM
- **CORS Protection**: Configurable origins

## 🎯 Key Features

### Multi-Level Approval Workflow
1. **Level 1**: Direct Manager
2. **Level 2**: Manager's Manager (if exists)
3. **Level 3**: HR Admin (for leaves > 5 days)

### Smart Leave Calculations
- Excludes weekends automatically
- Excludes company holidays
- Prevents overlapping requests
- Real-time balance updates

### Balance Management
- **Total Days**: Annual quota
- **Used Days**: Approved leaves
- **Pending Days**: Awaiting approval
- **Available Days**: Total - Used - Pending

## 🔄 Development Workflow

### Modular Structure (In Progress)
The codebase is being reorganized into a modular structure:
- Current: `legacy_main.py` (single file - working)
- Future: Modular `main.py` with separate routers

### Adding New Features
1. Define model in `app/models/`
2. Create schema in `app/schemas/`
3. Add business logic in `app/services/`
4. Create router in `app/routers/`
5. Register router in `app/main.py`

## 📖 API Documentation

Access interactive API documentation:
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

## 🐛 Debugging

Enable debug mode in `run.py`:
```python
uvicorn.run(..., reload=True, log_level="debug")
```

## 📝 Notes

- Database file will be created on first run
- Seed data is automatically inserted
- Hot reload is enabled in development
- CORS is configured for frontend (port 3000)

---

**For frontend integration**: The API is configured to work with the React frontend at http://localhost:3000
