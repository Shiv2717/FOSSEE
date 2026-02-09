# 📋 Deployment Checklist

Use this checklist to ensure your deployment is successful. Check off items as you complete them.

## 🔧 Pre-Deployment Setup

- [ ] Repository uploaded to GitHub
- [ ] `.env` and sensitive files added to `.gitignore`
- [ ] Run `python docs/deployment/generate_secret_key.py` and save the key
- [ ] Update GitHub repository with deployment files:
  - [ ] `chemical_visualizer/Procfile` created
  - [ ] `chemical_visualizer/runtime.txt` created
  - [ ] `chemical_visualizer/requirements_production.txt` updated
  - [ ] All changes committed and pushed to GitHub

## Backend Deployment (Render) ☁️

### Step 1: Create Database
- [ ] Go to [render.com/dashboard](https://render.com/dashboard)
- [ ] Create PostgreSQL instance or use Render's built-in DB
- [ ] Note down: DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

### Step 2: Deploy Backend Service
- [ ] Create New Web Service
- [ ] Connect GitHub repository
- [ ] Select `FOSSENN` repository
- [ ] Set Root Directory to `chemical_visualizer`
- [ ] Configure Build & Start Commands as per docs/deployment/QUICK_DEPLOY.md
- [ ] Add Environment Variables (from docs/deployment/.env.production.example):
  - [ ] DEBUG = False
  - [ ] SECRET_KEY = (from docs/deployment/generate_secret_key.py)
  - [ ] DB_ENGINE = django.db.backends.postgresql
  - [ ] DB_NAME = (from PostgreSQL setup)
  - [ ] DB_USER = (from PostgreSQL setup)
  - [ ] DB_PASSWORD = (from PostgreSQL setup)
  - [ ] DB_HOST = (from PostgreSQL setup)
  - [ ] API_USERNAME = admin
  - [ ] API_PASSWORD = (secure password)
  - [ ] CORS_ALLOWED_ORIGINS = (will update after frontend deploy)

### Step 3: Verify Backend
- [ ] Wait for deployment to complete
- [ ] Copy service URL (e.g., `your-app-name.onrender.com`)
- [ ] Test API: `https://your-app-name.onrender.com/api/`
- [ ] Verify CORS is working

## Frontend Deployment (Vercel) 🚀

### Step 1: Prepare Frontend
- [ ] Create `react_frontend/.env.production` file
- [ ] Set REACT_APP_API_URL to your Render backend URL
- [ ] Set REACT_APP_API_USERNAME and REACT_APP_API_PASSWORD
- [ ] Commit and push to GitHub

### Step 2: Deploy Frontend
- [ ] Go to [vercel.com](https://vercel.com)
- [ ] Create New Project
- [ ] Import FOSSENN repository
- [ ] Set Root Directory to `react_frontend`
- [ ] Add Environment Variables:
  - [ ] REACT_APP_API_URL = https://your-render-app.onrender.com
  - [ ] REACT_APP_API_USERNAME = admin
  - [ ] REACT_APP_API_PASSWORD = (same as backend)
- [ ] Deploy and wait for completion
- [ ] Copy Vercel domain (e.g., `your-app-name.vercel.app`)

### Step 3: Verify Frontend
- [ ] Open `https://your-app-name.vercel.app`
- [ ] Login with credentials
- [ ] Try uploading a CSV file
- [ ] Verify charts display correctly

## Post-Deployment Configuration 🔒

### Step 1: Update Backend CORS
- [ ] Go to Render Dashboard → Your Backend Service
- [ ] Click Environment Variables
- [ ] Update CORS_ALLOWED_ORIGINS:
  ```
  https://your-vercel-domain.vercel.app,http://localhost:3000
  ```
- [ ] Redeploy service (automatic)

### Step 2: Test End-to-End
- [ ] Frontend loads without errors
- [ ] File upload works
- [ ] Download report/PDF is possible
- [ ] Check Render logs for errors

### Step 3: Create Admin User (if needed)
- [ ] Go to Render Dashboard → Backend Service → Shell
- [ ] Run:
  ```bash
  python manage.py shell
  >>> from django.contrib.auth.models import User
  >>> User.objects.create_superuser('admin', 'admin@example.com', 'secure-password')
  >>> exit()
  ```
- [ ] Test login with new credentials

## Desktop App Distribution 📦

- [ ] Install PyInstaller: `pip install pyinstaller`
- [ ] Build executable: `pyinstaller --onefile --windowed desktop_app.py`
- [ ] Update `.env` in desktop app with production URLs
- [ ] Test executable on clean Windows machine
- [ ] Create GitHub Release and upload `desktop_app.exe`

## Security Review 🔐

- [ ] DEBUG set to False in production
- [ ] SECRET_KEY changed from default
- [ ] Credentials not hardcoded anywhere
- [ ] `.gitignore` includes sensitive files
- [ ] SSL certificates active (automatic)
- [ ] CORS origins restricted to your domain
- [ ] Database password is strong
- [ ] Admin password is strong and NOT default

## Monitoring & Maintenance 📊

- [ ] Set up error monitoring (optional: Sentry)
- [ ] Check Render logs weekly
- [ ] Monitor Vercel deployment status
- [ ] Test file uploads periodically
- [ ] Backup database regularly
- [ ] Review and update dependencies monthly

## Rollback Plan 🔄

- [ ] Keep previous stable commit tags
- [ ] Document any production issues
- [ ] Test rollback procedure before going live
- [ ] Know how to quickly revert on Render/Vercel

## Final Sign-Off ✅

- [ ] All tests passed
- [ ] Performance acceptable
- [ ] No console errors
- [ ] Users can login
- [ ] Users can upload files
- [ ] Reports generate correctly
- [ ] Team informed of live URL

---

## 📞 Quick Reference

| What | Link |
|------|------|
| Backend URL | https://your-app-name.onrender.com |
| Frontend URL | https://your-app-name.vercel.app |
| Render Dashboard | https://render.com/dashboard |
| Vercel Dashboard | https://vercel.com/dashboard |
| GitHub Repo | https://github.com/your-username/FOSSENN |
| Admin Username | admin |
| Admin Password | (see .env) |

---

**🎉 When all items are checked, your application is ready for production!**
