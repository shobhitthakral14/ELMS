# 🚀 ELMS Quick Reference Card

## 📍 Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend App** | http://localhost:3000 | Main application |
| **Backend API** | http://localhost:8001 | REST API |
| **API Docs** | http://localhost:8001/docs | Swagger UI |
| **Health Check** | http://localhost:8001/health | Server status |

## 🔐 Test Credentials

| Role | Email | Password |
|------|-------|----------|
| Employee | employee@company.com | employee123 |
| Manager | manager@company.com | manager123 |
| HR Admin | admin@company.com | admin123 |

## 🚀 Start Commands

### Backend
```bash
cd backend
python run.py
```

### Frontend
```bash
cd frontend
npm run dev
```

## 📁 File Locations

| What | Where |
|------|-------|
| Backend Code | `backend/app/` |
| Frontend Pages | `frontend/src/pages/` |
| API Client | `frontend/src/services/api/` |
| Database | `backend/leave_management.db` |
| Config | `backend/app/config.py` |

## 🔧 Common Tasks

### Add New API Endpoint
1. Create model: `backend/app/models/`
2. Add schema: `backend/app/schemas/`
3. Create router: `backend/app/routers/`
4. Register in: `backend/app/main.py`

### Add New Page
1. Create: `frontend/src/pages/NewPage.jsx`
2. Add route: `frontend/src/App.jsx`
3. Update: `frontend/src/constants/routes.js`

### Reset Database
```bash
cd backend
rm leave_management.db
python run.py  # Recreates with seed data
```

## 🐛 Quick Fixes

### Backend Issues
```bash
cd backend
pip install -r requirements.txt --force-reinstall
```

### Frontend Issues
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Port Already in Use
```bash
# Kill process on port 8001
npx kill-port 8001

# Kill process on port 3000
npx kill-port 3000
```

## 📖 Documentation

| File | Purpose |
|------|---------|
| `START_HERE.md` | Quick start guide |
| `README.md` | Full documentation |
| `CLEANUP_SUMMARY.md` | What was cleaned |
| `VERIFICATION_REPORT.md` | Test results |
| `PROJECT_STRUCTURE.md` | Structure guide |

## ✅ Quick Health Check

```bash
# Backend
curl http://localhost:8001/health

# Frontend
curl http://localhost:3000

# Login test
curl -X POST http://localhost:8001/auth/login \
  -d "username=employee@company.com&password=employee123"
```

---

**Keep this card handy for quick reference!** 📌
