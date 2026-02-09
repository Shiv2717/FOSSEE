# Quick Setup Guide - Production Ready

This is a quick start guide for the Chemical Equipment Visualizer. For comprehensive deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## 🚀 Quick Start (Single Command)

### All Components at Once

**Windows:**
```bash
scripts\start_all.bat
```

**Linux/Mac:**
```bash
./scripts/start_backend.sh & ./scripts/start_frontend.sh &
```

This automatically starts backend, frontend, and desktop app with all dependencies configured.

---

## 📦 Manual Setup (First Time)

## 📦 Manual Setup (First Time)

### Step 1: Install Dependencies

**Backend:**
```bash
cd chemical_visualizer
pip install -r requirements.txt
pip install -r desktop_requirements.txt
```

**Frontend:**
```bash
cd react_frontend
npm install
```

### Step 2: Configure Environment

**Copy environment templates:**
```bash
# Backend
cp chemical_visualizer/.env.example chemical_visualizer/.env

# Frontend
cp react_frontend/.env.example react_frontend/.env
```

**Update credentials in `.env` files** (optional for development, required for production)

### Step 3: Initialize Database

```bash
cd chemical_visualizer
python manage.py migrate
```

---

## 🎯 Running the Application

### Development Mode

**Individual Components:**
```bash
# Windows
scripts\start_backend.bat      # Backend API on port 8000
scripts\start_frontend.bat     # React app on port 3000
scripts\start_desktop.bat      # Desktop application

# Linux/Mac
./scripts/start_backend.sh
./scripts/start_frontend.sh
./scripts/start_desktop.sh
```

### Production Mode

**Windows:**
```bash
scripts\start_production.bat
```

**Linux/Mac:**
```bash
./scripts/start_production.sh
```

Uses Gunicorn (Linux/Mac) or Waitress (Windows) for production-grade serving.

---

## 🔐 Authentication

### Default Credentials (Development)
- **Username:** admin
- **Password:** admin123

### Production Setup
Update credentials in `.env` files:
```env
# chemical_visualizer/.env
API_USERNAME=your_admin_username
API_PASSWORD=your_secure_password

# react_frontend/.env
REACT_APP_API_USERNAME=your_admin_username
REACT_APP_API_PASSWORD=your_secure_password
```

---

## 📊 Using Real Data

### No Test Data Required!

This application is production-ready and works with real data:

1. **Prepare your CSV file** with required columns:
   - `equipment_id`, `equipment_type`, `flowrate`, `pressure`, `temperature`, `timestamp`

2. **Upload via:**
   - Web interface: http://localhost:3000
   - Desktop app
   - Direct API:
     ```bash
     curl -u admin:password -F "csv_file=@data.csv" http://localhost:8000/api/upload/
     ```

### Sample Data (Optional)
```bash
cd chemical_visualizer
python create_sample_csv.py  # Generates test_equipment.csv
```

---

## 📝 Important Files

| File | Purpose |
|------|---------|
| `.env` | Environment configuration |
| `DEPLOYMENT.md` | Comprehensive deployment guide |
| `QUICK_REFERENCE.md` | Command reference |
| `test_equipment.csv` | Sample data file (optional) |

## 🔗 Access Points

- **Backend API:** http://localhost:8000/api/
- **Django Admin:** http://localhost:8000/admin/
- **Web App:** http://localhost:3000
- **Desktop App:** Run via `start_desktop.bat` or `.sh`

---

**Ready to go!** 🚀 Run `start_all.bat` (Windows) or `./start_backend.sh` (Linux/Mac) to begin.

For detailed deployment, see [DEPLOYMENT.md](DEPLOYMENT.md) | Quick commands: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)