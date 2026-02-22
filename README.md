# HR Leave Management System (ELMS)

A complete, production-ready employee leave management system with FastAPI backend and React frontend.

## 📖 Overview

ELMS is a full-stack application for managing employee leave requests with multi-level approval workflows. It includes role-based access control, real-time balance tracking, and comprehensive reporting features.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         ELMS System                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────┐              ┌─────────────────┐          │
│  │                 │              │                 │          │
│  │   React         │◄────HTTP────►│   FastAPI      │          │
│  │   Frontend      │              │   Backend      │          │
│  │   (Port 3000)   │              │   (Port 8001)  │          │
│  │                 │              │                 │          │
│  └─────────────────┘              └────────┬────────┘          │
│                                             │                    │
│                                             ▼                    │
│                                    ┌─────────────────┐          │
│                                    │                 │          │
│                                    │   SQLite DB     │          │
│                                    │                 │          │
│                                    └─────────────────┘          │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
elms/
├── backend/                     # FastAPI Backend
│   ├── app/                    # Application package
│   │   ├── models/            # Database models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── routers/           # API endpoints
│   │   ├── services/          # Business logic
│   │   ├── utils/             # Utilities
│   │   ├── config.py          # Configuration
│   │   ├── database.py        # DB setup
│   │   ├── main.py            # Main app (modular)
│   │   └── legacy_main.py     # Current implementation
│   ├── leave_management.db    # SQLite database
│   ├── requirements.txt       # Python dependencies
│   ├── run.py                 # Server entry point
│   └── README.md              # Backend docs
│
├── frontend/                    # React Frontend
│   ├── src/
│   │   ├── pages/             # Page components
│   │   ├── components/        # Reusable components
│   │   ├── services/          # API client
│   │   ├── constants/         # Configuration
│   │   ├── hooks/             # Custom hooks
│   │   ├── App.jsx            # Main component
│   │   └── main.jsx           # Entry point
│   ├── package.json           # Node dependencies
│   ├── vite.config.js         # Vite config
│   └── README.md              # Frontend docs
│
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- pip
- npm

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Run the backend server
python run.py
```

Backend will start on **http://localhost:8001**

### 2. Frontend Setup

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install Node dependencies
npm install

# Run the frontend dev server
npm run dev
```

Frontend will start on **http://localhost:3000**

### 3. Access the Application

Open your browser and go to:
```
http://localhost:3000
```

## 🔑 Default Credentials

| Role | Email | Password | Permissions |
|------|-------|----------|-------------|
| **HR Admin** | admin@company.com | admin123 | Full system access |
| **Manager** | manager@company.com | manager123 | Team management + approvals |
| **Employee** | employee@company.com | employee123 | Submit requests |

## ✨ Features

### For Employees
- ✅ Submit leave requests
- 📊 View leave balances (Available/Used/Pending)
- 📋 Track request status
- ❌ Cancel pending requests
- 📅 View company holidays

### For Managers
- ✅ Approve/reject team requests
- 👥 View team members' balances
- 💬 Add approval comments
- 🔄 Delegate approval authority
- 📊 Team leave calendar

### For HR Admins
- 👤 Manage users and roles
- 📝 Configure leave types
- 🎯 Initialize annual balances
- 🗓️ Manage holiday calendar
- 📊 View department-wise reports
- 📈 Leave usage analytics

## 🎯 Key Features

### 1. Multi-Level Approval Workflow
- **Level 1**: Direct Manager
- **Level 2**: Manager's Manager (if applicable)
- **Level 3**: HR Admin (for requests > 5 days)

### 2. Smart Leave Calculations
- Automatically excludes weekends
- Excludes company holidays
- Prevents overlapping requests
- Real-time balance updates

### 3. Role-Based Access Control
- Employee: Basic access
- Manager: Team management
- HR Admin: Full system control

### 4. Balance Management
- **Total Days**: Annual quota
- **Used Days**: Approved leaves
- **Pending Days**: Awaiting approval
- **Available Days**: Total - Used - Pending

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI
- **Database**: SQLite (SQLAlchemy ORM)
- **Authentication**: JWT + bcrypt
- **Validation**: Pydantic
- **API Docs**: Swagger UI / ReDoc

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Styling**: CSS3 (Component-scoped)

## 📡 API Documentation

Access interactive API documentation:

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **Health Check**: http://localhost:8001/health

### Main Endpoints

```
Authentication
POST   /auth/login              Login and get JWT token
POST   /auth/register           Register new user (HR only)
GET    /auth/me                 Get current user info

Leave Management
GET    /leave-types             List all leave types
GET    /leave-balances/me       Get my balances
POST   /leave-requests          Submit leave request
GET    /leave-requests          List leave requests
DELETE /leave-requests/{id}     Cancel leave request

Approvals
GET    /leave-requests/pending-approvals   Get pending for me
POST   /approvals/{id}/approve             Approve request
POST   /approvals/{id}/reject              Reject request

Reports (HR Admin)
GET    /reports/team-calendar              Team leave calendar
GET    /reports/leave-summary              Usage summary
GET    /reports/pending-requests           All pending requests
```

## 🗄️ Database Schema

### Core Tables
- **users**: Employee information and roles
- **leave_types**: Leave categories (Annual, Sick, etc.)
- **leave_balances**: Per-user leave balances by year
- **leave_requests**: All leave requests
- **approval_workflow**: Multi-level approval chain
- **holidays**: Company holiday calendar
- **delegations**: Temporary approval authority delegation

### Relationships
```
User
  ├── has many: LeaveBalance
  ├── has many: LeaveRequest
  ├── manages: User (as manager)
  └── created: Holiday

LeaveRequest
  ├── belongs to: User
  ├── belongs to: LeaveType
  └── has many: ApprovalWorkflow

ApprovalWorkflow
  ├── belongs to: LeaveRequest
  └── belongs to: User (as approver)
```

## 🔒 Security Features

- **JWT Authentication**: Secure token-based auth with 24-hour expiration
- **Password Hashing**: bcrypt for secure password storage
- **Role-Based Authorization**: Granular access control
- **SQL Injection Prevention**: SQLAlchemy ORM parameterized queries
- **CORS Protection**: Configured for frontend origin
- **Input Validation**: Pydantic schemas for all requests

## 📊 Workflow Example

### Leave Request Flow

```
1. Employee submits leave request
   ↓
2. System validates:
   - Sufficient balance
   - No overlapping requests
   - Working days calculation
   ↓
3. Create approval workflow:
   - Level 1: Manager
   - Level 2: Senior Manager (if exists)
   - Level 3: HR Admin (if > 5 days)
   ↓
4. Manager reviews and approves
   ↓
5. If additional levels: Continue approval chain
   ↓
6. Final approval: Update balance
   - Move pending → used
   - Send notification (future)
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest
```

### Frontend Testing
```bash
cd frontend
npm run test
```

### Manual Testing
1. Login as Employee → Submit request
2. Login as Manager → Approve request
3. Login as Employee → Check updated balance

## 📝 Development

### Adding New Features

#### Backend
1. Create model in `backend/app/models/`
2. Add schema in `backend/app/schemas/`
3. Implement logic in `backend/app/services/`
4. Create router in `backend/app/routers/`
5. Register router in `main.py`

#### Frontend
1. Create page in `frontend/src/pages/`
2. Add route in `App.jsx`
3. Implement API calls in `services/api/`
4. Update constants if needed

### Code Style

#### Backend
- Follow PEP 8
- Use type hints
- Document with docstrings
- Keep functions focused

#### Frontend
- Use functional components
- Implement hooks for state
- Keep components focused
- Use meaningful names

## 🐛 Troubleshooting

### Backend Issues

**Database locked**
```bash
# Stop the server and delete database
rm backend/leave_management.db
# Restart server (will recreate with seed data)
python backend/run.py
```

**Import errors**
```bash
cd backend
pip install -r requirements.txt --force-reinstall
```

### Frontend Issues

**Cannot connect to backend**
- Ensure backend is running on port 8001
- Check `API_BASE_URL` in `frontend/src/constants/api.js`
- Verify CORS settings in backend

**Dependencies error**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 🚀 Deployment

### Backend Deployment

**Option 1: Docker**
```bash
cd backend
docker build -t elms-backend .
docker run -p 8001:8001 elms-backend
```

**Option 2: Cloud Platform**
- Deploy to Heroku, AWS, or Google Cloud
- Use PostgreSQL instead of SQLite
- Set environment variables for production

### Frontend Deployment

**Build for production**
```bash
cd frontend
npm run build
```

**Deploy to**:
- Netlify
- Vercel
- AWS S3 + CloudFront
- GitHub Pages

### Environment Configuration

**Backend (.env)**
```bash
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:pass@host/db
```

**Frontend (.env)**
```bash
VITE_API_URL=https://api.yourdomain.com
```

## 📚 Documentation

- **Backend API**: http://localhost:8001/docs
- **Backend README**: `backend/README.md`
- **Frontend README**: `frontend/README.md`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🎓 Learning Resources

### FastAPI
- Official Docs: https://fastapi.tiangolo.com/
- Tutorial: https://fastapi.tiangolo.com/tutorial/

### React
- Official Docs: https://react.dev/
- React Router: https://reactrouter.com/

### SQLAlchemy
- Official Docs: https://docs.sqlalchemy.org/

## ⭐ Features Roadmap

### Phase 1 (Current)
- ✅ Basic leave management
- ✅ Multi-level approvals
- ✅ Balance tracking
- ✅ Role-based access

### Phase 2 (Planned)
- 📧 Email notifications
- 📎 Document attachments
- 📊 Advanced analytics
- 🔔 Real-time notifications

### Phase 3 (Future)
- 📱 Mobile app
- 🔗 Calendar integration (Google/Outlook)
- 📈 Predictive analytics
- 🌍 Multi-language support

## 💬 Support

For issues or questions:
- Create an issue on GitHub
- Check documentation in `README.md` files
- Review API docs at `/docs` endpoint

---

**Built with ❤️ for efficient leave management**

**Current Version**: 1.0.0
**Last Updated**: 2026-02-22
