# 📁 ELMS - Organized Project Structure

## 🎯 Overview
The project is now fully organized with clear separation between backend and frontend, modular code structure, and comprehensive documentation.

---

## 📂 Complete Folder Structure

```
elms/
│
├── 📁 backend/                          # Backend Application
│   ├── 📁 app/                         # Main application package
│   │   ├── 📁 models/                  # Database Models (ORM)
│   │   │   ├── __init__.py            # Export all models
│   │   │   ├── user.py                # User model
│   │   │   ├── leave.py               # Leave-related models
│   │   │   ├── holiday.py             # Holiday model
│   │   │   └── delegation.py          # Delegation model
│   │   │
│   │   ├── 📁 schemas/                 # Pydantic Schemas (Validation)
│   │   │   ├── __init__.py            # Export all schemas
│   │   │   ├── enums.py               # Enum definitions
│   │   │   ├── user.py                # User schemas
│   │   │   ├── leave.py               # Leave schemas
│   │   │   ├── holiday.py             # Holiday schemas
│   │   │   └── delegation.py          # Delegation schemas
│   │   │
│   │   ├── 📁 routers/                 # API Routers (Endpoints)
│   │   │   ├── __init__.py            # Export all routers
│   │   │   ├── auth.py                # Authentication endpoints
│   │   │   ├── users.py               # User management
│   │   │   ├── leave_types.py         # Leave types
│   │   │   ├── leave_balances.py      # Leave balances
│   │   │   ├── leave_requests.py      # Leave requests
│   │   │   ├── approvals.py           # Approval workflow
│   │   │   ├── holidays.py            # Holidays
│   │   │   ├── delegations.py         # Delegations
│   │   │   └── reports.py             # Reports
│   │   │
│   │   ├── 📁 services/                # Business Logic
│   │   │   ├── __init__.py            # Export all services
│   │   │   ├── auth_service.py        # Authentication logic
│   │   │   ├── leave_service.py       # Leave workflow logic
│   │   │   └── seed_service.py        # Database seeding
│   │   │
│   │   ├── 📁 utils/                   # Utility Functions
│   │   │   ├── __init__.py            # Export utilities
│   │   │   ├── auth.py                # JWT & password utilities
│   │   │   └── helpers.py             # Helper functions
│   │   │
│   │   ├── __init__.py                # Package init
│   │   ├── config.py                  # ⚙️  Configuration settings
│   │   ├── database.py                # 🗄️  Database setup
│   │   ├── main.py                    # 🚀 Main app (modular)
│   │   └── legacy_main.py             # 📄 Current working version
│   │
│   ├── 🗄️ leave_management.db         # SQLite Database
│   ├── 📄 requirements.txt             # Python dependencies
│   ├── 🚀 run.py                       # Server entry point
│   └── 📖 README.md                    # Backend documentation
│
├── 📁 frontend/                         # Frontend Application
│   ├── 📁 public/                      # Static assets
│   │
│   ├── 📁 src/                         # Source code
│   │   ├── 📁 pages/                   # Page Components (Routes)
│   │   │   ├── Login.jsx              # 🔐 Login page
│   │   │   ├── Login.css              # Login styles
│   │   │   ├── Dashboard.jsx          # 📊 Dashboard
│   │   │   ├── Dashboard.css          # Dashboard styles
│   │   │   ├── LeaveRequest.jsx       # 📝 Submit request
│   │   │   ├── LeaveRequest.css       # Request styles
│   │   │   ├── LeaveList.jsx          # 📋 View requests
│   │   │   ├── LeaveList.css          # List styles
│   │   │   ├── Approvals.jsx          # ✅ Approve/reject
│   │   │   └── Approvals.css          # Approvals styles
│   │   │
│   │   ├── 📁 components/              # Reusable UI Components
│   │   │   └── (original files - can be cleaned)
│   │   │
│   │   ├── 📁 services/                # External Services
│   │   │   └── api/
│   │   │       └── api.js             # 🌐 Backend API client
│   │   │
│   │   ├── 📁 constants/               # Configuration Constants
│   │   │   ├── api.js                 # API endpoints & config
│   │   │   └── routes.js              # Route definitions
│   │   │
│   │   ├── 📁 hooks/                   # Custom React Hooks
│   │   │   └── (future custom hooks)
│   │   │
│   │   ├── App.jsx                    # 🎯 Main app component
│   │   ├── App.css                    # App styles
│   │   ├── main.jsx                   # 🚀 Entry point
│   │   └── index.css                  # 🎨 Global styles
│   │
│   ├── index.html                      # HTML template
│   ├── package.json                    # Node dependencies
│   ├── vite.config.js                  # ⚙️  Vite configuration
│   └── 📖 README.md                    # Frontend documentation
│
├── 📖 README.md                         # Main project documentation
└── 📄 PROJECT_STRUCTURE.md             # This file
```

---

## 🏗️ Architecture Layers

### Backend Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Backend Layers                      │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  1. 🌐 API Layer (routers/)                            │
│     └─> Handle HTTP requests/responses                  │
│                                                           │
│  2. 📋 Validation Layer (schemas/)                      │
│     └─> Pydantic models for data validation            │
│                                                           │
│  3. 💼 Business Logic Layer (services/)                 │
│     └─> Core business rules & workflows                 │
│                                                           │
│  4. 🔧 Utility Layer (utils/)                           │
│     └─> Helper functions & utilities                    │
│                                                           │
│  5. 🗄️ Data Layer (models/)                            │
│     └─> SQLAlchemy ORM models                          │
│                                                           │
│  6. 💾 Database (database.py)                           │
│     └─> SQLite connection & sessions                    │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### Frontend Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend Layers                      │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  1. 📱 Pages Layer (pages/)                             │
│     └─> Route-specific page components                  │
│                                                           │
│  2. 🧩 Components Layer (components/)                   │
│     └─> Reusable UI components                          │
│                                                           │
│  3. 🔌 Services Layer (services/)                       │
│     └─> API integration & external services             │
│                                                           │
│  4. 🎣 Hooks Layer (hooks/)                             │
│     └─> Custom React hooks                              │
│                                                           │
│  5. ⚙️ Constants Layer (constants/)                     │
│     └─> Configuration & constants                        │
│                                                           │
│  6. 🎨 Styles Layer (CSS files)                         │
│     └─> Component & global styles                       │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 📖 Key Files Explained

### Backend Files

| File | Purpose |
|------|---------|
| `run.py` | 🚀 Entry point to start the server |
| `app/config.py` | ⚙️ All configuration settings |
| `app/database.py` | 🗄️ Database connection & sessions |
| `app/main.py` | 🎯 FastAPI app initialization |
| `app/legacy_main.py` | 📄 Current working monolithic version |
| `app/models/*.py` | 🗂️ Database table definitions |
| `app/schemas/*.py` | ✅ Request/response validation |
| `app/routers/*.py` | 🛣️ API endpoint handlers |
| `app/services/*.py` | 💼 Business logic & workflows |
| `app/utils/*.py` | 🔧 Helper & utility functions |

### Frontend Files

| File | Purpose |
|------|---------|
| `main.jsx` | 🚀 Application entry point |
| `App.jsx` | 🎯 Main app with routing |
| `pages/*.jsx` | 📄 Page components for routes |
| `services/api/api.js` | 🌐 Backend API integration |
| `constants/api.js` | ⚙️ API endpoints & config |
| `constants/routes.js` | 🛣️ Route definitions |
| `*.css` | 🎨 Component & global styles |

---

## 🚀 How to Run

### Backend
```bash
cd backend
pip install -r requirements.txt
python run.py
```
✅ Server starts on **http://localhost:8001**

### Frontend
```bash
cd frontend
npm install
npm run dev
```
✅ App starts on **http://localhost:3000**

---

## 🎯 Code Organization Benefits

### ✅ Backend Benefits
- **Separation of Concerns**: Each layer has a specific responsibility
- **Maintainability**: Easy to find and update specific functionality
- **Scalability**: Simple to add new features without breaking existing code
- **Testability**: Each module can be tested independently
- **Clarity**: Clear structure makes onboarding easier

### ✅ Frontend Benefits
- **Component Isolation**: Each page is self-contained
- **Reusability**: Common components can be shared
- **API Centralization**: All API calls in one place
- **Constants Management**: Configuration is centralized
- **Easy Navigation**: Clear folder structure

---

## 📚 Documentation

- **Main README**: Project overview and quick start
- **Backend README**: Detailed backend architecture & API docs
- **Frontend README**: Frontend structure & development guide
- **This File**: Complete project structure reference

---

## 🔄 Development Workflow

### Adding a New Feature

#### Backend
1. Create model in `app/models/`
2. Add schema in `app/schemas/`
3. Write business logic in `app/services/`
4. Create router in `app/routers/`
5. Register router in `app/main.py`

#### Frontend
1. Create page in `src/pages/`
2. Add API functions in `src/services/api/`
3. Define routes in `src/constants/routes.js`
4. Add route in `App.jsx`
5. Style with component CSS

---

## ✨ Current Status

- ✅ Backend fully organized with modular structure
- ✅ Frontend reorganized with clear separation
- ✅ Comprehensive documentation for all layers
- ✅ Both servers running successfully
- ✅ All features working as expected
- ✅ Easy to understand and maintain

---

## 🎉 You Can Now

1. **Navigate easily**: Find any file quickly with clear structure
2. **Understand code**: Each file has a specific purpose
3. **Add features**: Follow the clear patterns established
4. **Maintain code**: Update specific parts without affecting others
5. **Scale project**: Add new modules without complexity

---

**🚀 Your organized ELMS project is ready for development!**

---

*For detailed information about each component, refer to the README files in backend/ and frontend/ directories.*
