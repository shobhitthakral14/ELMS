# 🚀 Quick Start Guide - ELMS

## ⚡ Start the Application (Both Servers)

### Option 1: Start Both Servers Simultaneously

**Windows (PowerShell):**
```powershell
# Terminal 1 - Backend
cd backend
python run.py

# Terminal 2 - Frontend (in a NEW terminal)
cd frontend
npm run dev
```

**Linux/Mac:**
```bash
# Terminal 1 - Backend
./start_backend.sh

# Terminal 2 - Frontend (in a NEW terminal)
./start_frontend.sh
```

### Option 2: Start Individually

#### Backend Only
```bash
cd backend
python run.py
```
✅ Backend will run on **http://localhost:8001**

#### Frontend Only
```bash
cd frontend
npm run dev
```
✅ Frontend will run on **http://localhost:3000**

---

## 🌐 Access the Application

Once both servers are running:

**Open your browser:**
```
http://localhost:3000
```

**Quick Login:**
- Employee: `employee@company.com` / `employee123`
- Manager: `manager@company.com` / `manager123`
- HR Admin: `admin@company.com` / `admin123`

---

## 📊 API Documentation

**Swagger UI:** http://localhost:8001/docs
**ReDoc:** http://localhost:8001/redoc
**Health Check:** http://localhost:8001/health

---

## 🔧 First Time Setup

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python run.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## ✅ Verify Connection

### Test Backend
```bash
curl http://localhost:8001/health
```
Should return: `{"status":"healthy","timestamp":"..."}`

### Test Frontend
Open: http://localhost:3000
Should see: Login page

---

## 🛑 Stopping Servers

Press `Ctrl + C` in each terminal window.

---

## 📁 Project Structure

```
elms/
├── backend/          # FastAPI backend (Port 8001)
├── frontend/         # React frontend (Port 3000)
├── README.md         # Full documentation
└── START_HERE.md     # This file
```

---

## 🐛 Troubleshooting

### Backend won't start
```bash
cd backend
pip install -r requirements.txt --force-reinstall
python run.py
```

### Frontend won't start
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### "Connection refused" error
- Make sure backend is running on port 8001
- Make sure frontend is running on port 3000
- Check firewall settings

### Database issues
- Delete `backend/leave_management.db`
- Restart backend (will recreate with seed data)

---

## 📖 More Information

- **Full Documentation:** See `README.md`
- **Backend Details:** See `backend/README.md`
- **Frontend Details:** See `frontend/README.md`
- **Structure Guide:** See `PROJECT_STRUCTURE.md`

---

**🎉 That's it! Your ELMS is ready to use!**
