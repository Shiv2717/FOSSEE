# Deployment Guide - Chemical Equipment Visualizer

## 🚀 Production Deployment Guide

This guide covers deploying the Chemical Equipment Visualizer for production use with real data.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Initial Setup](#initial-setup)
- [Environment Configuration](#environment-configuration)
- [Database Setup](#database-setup)
- [Running in Production](#running-in-production)
- [Deployment Options](#deployment-options)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- Python 3.8+ with pip
- Node.js 14+ with npm
- 2GB RAM minimum
- 1GB disk space

### Install Dependencies
```bash
# 1. Install Python dependencies
cd chemical_visualizer
pip install -r requirements.txt

# 2. Install React dependencies
cd ../react_frontend
npm install

# 3. Install Desktop App dependencies (optional)
cd ../chemical_visualizer
pip install -r desktop_requirements.txt
```

---

## Initial Setup

### 1. Clone and Navigate to Project
```bash
cd FOSSENN
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install All Dependencies
```bash
# Backend
pip install -r chemical_visualizer/requirements.txt

# Desktop (optional)
pip install -r chemical_visualizer/desktop_requirements.txt

# Frontend
cd react_frontend
npm install
cd ..
```

---

## Environment Configuration

### 1. Copy Environment Files
```bash
# Backend
cp chemical_visualizer/.env.example chemical_visualizer/.env

# Frontend
cp react_frontend/.env.example react_frontend/.env

# Root (optional)
cp .env.example .env
```

### 2. Configure Backend (`chemical_visualizer/.env`)

**CRITICAL: Update these values for security!**

```env
# Django Settings
SECRET_KEY=your-very-long-random-secret-key-generate-one
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-server-ip

# Database (SQLite for now, PostgreSQL recommended for production)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# API Credentials - CHANGE THESE!
API_USERNAME=your_admin_username
API_PASSWORD=your_strong_secure_password

# CORS (add your frontend domains)
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**Generate a Secret Key:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Configure Frontend (`react_frontend/.env`)

```env
REACT_APP_API_URL=https://your-api-domain.com
REACT_APP_API_USERNAME=your_admin_username
REACT_APP_API_PASSWORD=your_strong_secure_password
```

---

## Database Setup

### 1. Run Migrations
```bash
cd chemical_visualizer
python manage.py migrate
```

### 2. Create Admin User
```bash
# Interactive mode
python manage.py createsuperuser

# OR use environment credentials
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'your_password')"
```

### 3. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

---

## Running in Production

### Option 1: Quick Start (All Components)

**Windows:**
```bash
start.bat
# OR for more control
scripts\start_all.bat
```

**Linux/Mac:**  
```bash
./start.sh
# OR for more control
./scripts/start_backend.sh & ./scripts/start_frontend.sh &
```

This starts:
- Backend on http://localhost:8000
- Frontend on http://localhost:3000
- Desktop app in separate window

### Option 2: Individual Components

**Backend (Production Server):**
```bash
# Windows
scripts\start_production.bat

# Linux/Mac
./scripts/start_production.sh
```

**Frontend (Development):**
```bash
# Windows
scripts\start_frontend.bat

# Linux/Mac
./scripts/start_frontend.sh
```

**Frontend (Production Build):**
```bash
# Windows
scripts\build_frontend.bat

# Linux/Mac
./scripts/build_frontend.sh
# Then serve the build folder with nginx, Apache, or serve package
```

**Desktop App:**
```bash
# Windows
scripts\start_desktop.bat

# Linux/Mac
./scripts/start_desktop.sh
```

### Option 3: Production Servers

**Backend with Gunicorn (Linux/Mac):**
```bash
cd chemical_visualizer
gunicorn chemical_visualizer.wsgi:application --bind 0.0.0.0:8000 --workers 3 --daemon
```

**Backend with Waitress (Windows):**
```bash
cd chemical_visualizer
waitress-serve --port=8000 chemical_visualizer.wsgi:application
```

---

## Deployment Options

### 1. Local Network Deployment

1. Start backend on server machine
2. Get server IP address: `ipconfig` (Windows) or `ifconfig` (Linux/Mac)
3. Update firewall to allow port 8000
4. Update `.env` files on client machines with server IP:
   ```env
   DESKTOP_API_URL=http://192.168.1.100:8000
   REACT_APP_API_URL=http://192.168.1.100:8000
   ```

### 2. Cloud Deployment (DigitalOcean, AWS, etc.)

**Backend (Django API):**
- Deploy using Gunicorn + Nginx
- Use PostgreSQL instead of SQLite
- Enable HTTPS with Let's Encrypt
- Set up systemd service for auto-restart

**Frontend (React):**
- Build: `npm run build`
- Deploy to Netlify, Vercel, or serve with Nginx
- Update API URL to production backend

**Database Migration to PostgreSQL:**
```bash
pip install psycopg2-binary
```

Update `chemical_visualizer/.env`:
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=chemical_db
DB_USER=postgres_user
DB_PASSWORD=postgres_password
DB_HOST=localhost
DB_PORT=5432
```

### 3. Windows Service (Background)

Use NSSM (Non-Sucking Service Manager):
```bash
# Download NSSM from nssm.cc
nssm install ChemicalVisualizerAPI "C:\path\to\.venv\Scripts\python.exe" "C:\path\to\chemical_visualizer\manage.py runserver 0.0.0.0:8000"
nssm start ChemicalVisualizerAPI
```

---

## Security Considerations

### ✅ Production Checklist

- [ ] **Change SECRET_KEY** - Generate unique secret key
- [ ] **Set DEBUG=False** - Never run DEBUG=True in production
- [ ] **Update ALLOWED_HOSTS** - Restrict to your domains
- [ ] **Change API Credentials** - Use strong passwords
- [ ] **Enable HTTPS** - Use SSL/TLS certificates
- [ ] **Restrict CORS** - Only allow trusted origins
- [ ] **Update .gitignore** - Never commit .env files
- [ ] **Regular Backups** - Backup database regularly
- [ ] **Update Dependencies** - Keep packages up to date
- [ ] **Rate Limiting** - Add API rate limiting
- [ ] **Logging** - Set up proper logging and monitoring

### Database Security

**For Production, Use PostgreSQL:**
```bash
# Install PostgreSQL
# Then install Python adapter
pip install psycopg2-binary

# Create database
createdb chemical_db

# Update settings for PostgreSQL connection
```

### API Authentication

Current: HTTP Basic Authentication
For Production Consider:
- Token-based authentication (JWT)
- OAuth2
- API Keys with expiration

---

## Using Real Data

### CSV File Requirements

Your CSV files must have these columns:
- `equipment_id` - Unique identifier
- `equipment_type` - Type of equipment
- `flowrate` - Flow rate value
- `pressure` - Pressure value
- `temperature` - Temperature value
- `timestamp` - Date/time of measurement

**Example CSV:**
```csv
equipment_id,equipment_type,flowrate,pressure,temperature,timestamp
PUMP-001,Pump,150.5,35.2,68.3,2024-01-15 10:30:00
VALVE-002,Valve,200.8,42.1,72.5,2024-01-15 10:31:00
```

### Upload Methods

1. **Web Interface:** http://localhost:3000
2. **Desktop App:** Click "Browse" button
3. **API Direct:**
   ```bash
   curl -X POST http://localhost:8000/api/upload/ \
     -u admin:password \
     -F "csv_file=@data.csv"
   ```

---

## Monitoring and Maintenance

### View API Admin Panel
```
http://localhost:8000/admin/
```

### Check Upload History
```bash
# Via API
curl -u admin:password http://localhost:8000/api/history/
```

### Generate Reports
```bash
# Via API
curl -u admin:password "http://localhost:8000/api/report/?equipment_id=PUMP-001" --output report.pdf
```

### Database Backup
```bash
# SQLite
cp chemical_visualizer/db.sqlite3 backups/db_$(date +%Y%m%d).sqlite3

# PostgreSQL
pg_dump chemical_db > backups/backup_$(date +%Y%m%d).sql
```

---

## Troubleshooting

### Backend Won't Start
```bash
# Check if port 8000 is already in use
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Apply migrations
python manage.py migrate

# Check logs
tail -f chemical_visualizer/logs/django.log  # If logging configured
```

### Frontend Connection Error
1. Verify backend is running: http://localhost:8000/api/history/
2. Check `.env` file has correct API URL
3. Verify CORS settings in backend
4. Check browser console for errors

### Desktop App Connection Error
1. Check `config.py` or `.env` file
2. Verify API URL is accessible
3. Test with curl:
   ```bash
   curl -u admin:password http://localhost:8000/api/history/
   ```

### Permission Denied
```bash
# Give execute permissions to scripts (Linux/Mac)
chmod +x start_*.sh
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r chemical_visualizer/requirements.txt --force-reinstall
```

---

## Performance Optimization

### Backend
- Use Gunicorn with multiple workers
- Enable caching (Redis/Memcached)
- Optimize database queries
- Use connection pooling

### Frontend
- Build for production: `npm run build`
- Enable compression
- Use CDN for static assets
- Implement lazy loading

### Database
- Add indexes on frequently queried columns
- Regular VACUUM (PostgreSQL)
- Monitor query performance

---

## Support and Maintenance

### Regular Tasks
- Daily: Check logs for errors
- Weekly: Backup database
- Monthly: Update dependencies, security patches
- Quarterly: Review and rotate credentials

### Logs Location
- Backend: `chemical_visualizer/logs/` (if configured)
- Frontend: Browser console
- Desktop: Application console output

---

## Additional Resources

- Django Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/
- React Production Build: https://create-react-app.dev/docs/production-build/
- Nginx Configuration Examples: https://www.nginx.com/resources/wiki/start/

---

**Ready for Production!** 🎉

For questions or issues, check the logs and troubleshooting section above.
