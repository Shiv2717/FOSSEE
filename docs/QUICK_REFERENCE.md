# Quick Reference - Chemical Equipment Visualizer

## 🚀 Start Commands

### Development Mode
```bash
# From project root

# Windows - All Components
scripts\start_all.bat

# Linux/Mac - All Components
./scripts/start_backend.sh & ./scripts/start_frontend.sh &

# Individual Components
scripts\start_backend.bat      # Django API
scripts\start_frontend.bat     # React App
scripts\start_desktop.bat      # PyQt5 Desktop
```

### Production Mode
```bash
# Windows
scripts\start_production.bat

# Linux/Mac
./scripts/start_production.sh
```

## 📋 Common Tasks

### Update Dependencies
```bash
# Windows
scripts\update_dependencies.bat

# Linux/Mac
./scripts/update_dependencies.sh
```

### Build Frontend for Production
```bash
# Windows
scripts\build_frontend.bat

# Linux/Mac
./scripts/build_frontend.sh
```

### Database Operations
```bash
cd chemical_visualizer

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Backup database
copy db.sqlite3 backups\db_backup.sqlite3  # Windows
cp db.sqlite3 backups/db_backup.sqlite3    # Linux/Mac
```

## 🔧 Configuration Files

- `.env` - Root environment variables
- `chemical_visualizer/.env` - Backend configuration
- `react_frontend/.env` - Frontend configuration
- `.env.example` files - Template for new deployments

## 📡 Application URLs

- **Backend API:** http://localhost:8000
- **API Admin:** http://localhost:8000/admin/
- **Frontend Web:** http://localhost:3000
- **API Docs:** http://localhost:8000/api/

## 🔐 Default Credentials

**Username:** admin  
**Password:** admin123

⚠️ **Change these in `.env` files for production!**

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/upload/` | POST | Upload CSV file |
| `/api/history/` | GET | Get upload history |
| `/api/report/?upload_id=1` | GET | Download PDF report |

## 📝 CSV Format

Required columns:
- `equipment_id` - Unique ID
- `equipment_type` - Type of equipment
- `flowrate` - Flow rate value
- `pressure` - Pressure value
- `temperature` - Temperature value
- `timestamp` - Date/time

## 🐛 Quick Troubleshooting

**Backend won't start:**
```bash
cd chemical_visualizer
python manage.py migrate
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

**Frontend connection issues:**
- Check `.env` has correct `REACT_APP_API_URL`
- Verify backend is running
- Check browser console for CORS errors

**Desktop app connection:**
- Verify `config.py` or `.env` has correct API URL
- Test with: `curl -u admin:admin123 http://localhost:8000/api/history/`

## 📚 Documentation

- **Full Setup:** [README.md](../README.md)
- **Deployment Guide:** [DEPLOYMENT.md](DEPLOYMENT.md)
- **Quick Setup:** [SETUP.md](SETUP.md)
- **Authentication:** `chemical_visualizer/AUTHENTICATION.md`

## 🛠️ Development

### Install Development Dependencies
```bash
# Backend
cd chemical_visualizer
pip install -r requirements.txt -r desktop_requirements.txt

# Frontend
cd react_frontend
npm install
```

### Run Tests
```bash
# Backend
cd chemical_visualizer
python manage.py test

# Frontend
cd react_frontend
npm test
```

## 📦 Production Checklist

- [ ] Copy `.env.example` files to `.env`
- [ ] Change `SECRET_KEY` in backend `.env`
- [ ] Set `DEBUG=False`
- [ ] Update `ALLOWED_HOSTS`
- [ ] Change API credentials
- [ ] Update CORS origins
- [ ] Build frontend: `npm run build`
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Set up SSL/HTTPS
- [ ] Configure firewall
- [ ] Set up regular database backups

## 💾 Backup Commands

```bash
# Database backup
cd chemical_visualizer
copy db.sqlite3 "backups\db_$(date +%Y%m%d).sqlite3"  # Windows
cp db.sqlite3 "backups/db_$(date +%Y%m%d).sqlite3"    # Linux/Mac

# Full project backup
cd ..
tar -czf backup_$(date +%Y%m%d).tar.gz FOSSENN/  # Linux/Mac
# Or use WinRAR/7-Zip on Windows
```

## 🔄 Update Production

```bash
# Pull latest changes
git pull origin main

# Update dependencies
update_dependencies.bat  # Windows
./update_dependencies.sh  # Linux/Mac

# Rebuild frontend
build_frontend.bat  # Windows
./build_frontend.sh  # Linux/Mac

# Restart services
start_production.bat  # Windows
./start_production.sh  # Linux/Mac
```

---

**For detailed information, see [DEPLOYMENT.md](DEPLOYMENT.md)**
