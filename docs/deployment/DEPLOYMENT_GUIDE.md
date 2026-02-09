# 🚀 Deployment Architecture & Getting Started

## 📊 System Architecture (Post-Deployment)

```
┌─────────────────────────────────────────────────────────────┐
│                    Internet Users                           │
└────────────────────────────────────────────────────────────┘
                          │
                          ├──────────────────┬──────────────────┐
                          │                  │                  │
                    [Vercel]          [Render]          [Desktop]
                 (Frontend React)   (Backend Django)   (PyQt5 App)
            your-app.vercel.app   your-app.onrender.com  (Local)
                    │                  │                  │
                    └──────────────────┼──────────────────┘
                                       │
                              [PostgreSQL Database]
                             (on Render or external)
```

---

## 🛠️ Quick Setup Command (Choose Your OS)

### **Windows:**
```batch
cd C:\Users\YourName\Desktop\FOSSENN
docs\deployment\prepare_deployment.bat
```

### **Linux/Mac:**
```bash
cd ~/Desktop/FOSSENN
chmod +x docs/deployment/prepare_deployment.sh
./docs/deployment/prepare_deployment.sh
```

---

## 📁 New Deployment Files Created

Your project now has these deployment-ready files:

```
FOSSENN/
├── chemical_visualizer/
│   ├── Procfile                              ← Render config
│   ├── runtime.txt                           ← Python version
│   ├── requirements_production.txt           ← Production deps
│   └── ...
│
├── react_frontend/
│   └── (needs .env.production)               ← CREATE THIS
│
├── docs/
│   ├── DEPLOYMENT.md                          ← Detailed guide
│   ├── SETUP.md
│   ├── PROJECT_INFO.md
│   ├── QUICK_REFERENCE.md
│   └── deployment/
│       ├── QUICK_DEPLOY.md                    ← Main guide (start here)
│       ├── DEPLOYMENT_CHECKLIST.md            ← Step-by-step checklist
│       ├── DEPLOYMENT_GUIDE.md                ← Architecture overview
│       ├── .env.production.example            ← Example env vars
│       ├── prepare_deployment.bat             ← Auto-setup (Windows)
│       ├── prepare_deployment.sh              ← Auto-setup (Linux/Mac)
│       └── generate_secret_key.py             ← Generate Django key
│
└── ...
```

---

## 🎯 Three Simple Deployment Paths

### **Path 1: Manual Setup (Recommended First Time)**
→ Read **docs/deployment/QUICK_DEPLOY.md** → Follow each step on Render & Vercel dashboards

### **Path 2: Using Preparation Script**
→ Run `docs/deployment/prepare_deployment.bat` or `docs/deployment/prepare_deployment.sh` → Finish GUI setup on Render/Vercel

### **Path 3: Full Automation (Advanced)**
→ Use Render's GitHub auto-deploy + Vercel's auto-deploy features

---

## ⚡ 5-Minute Quick Start

### **1. GitHub Preparation (5-10 min)**
```bash
# Ensure all files are committed
git add .
git commit -m "Add deployment configuration"
git push origin main
```

### **2. Backend Deployment (10 min)**
1. Go to [render.com](https://render.com) → Sign up with GitHub
2. Create New Web Service
3. Select FOSSENN repository
4. Fill in: Name, Root Directory (`chemical_visualizer`), Python 3
5. Add Environment Variables (copy from docs/deployment/.env.production.example)
6. Deploy and wait ⏳

**Your Backend URL:** `https://your-app-name.onrender.com`

### **3. Frontend Deployment (5 min)**
1. Go to [vercel.com](https://vercel.com) → Sign up with GitHub
2. Create New Project
3. Select FOSSENN repository
4. Set Root Directory to `react_frontend`
5. Add Environment Variables:
   ```
   REACT_APP_API_URL = https://your-app-name.onrender.com
   REACT_APP_API_USERNAME = admin
   REACT_APP_API_PASSWORD = <your-password>
   ```
6. Deploy ✅

**Your Frontend URL:** `https://your-app-name.vercel.app`

### **4. Connect Frontend to Backend (1 min)**
Go back to Render → Update CORS_ALLOWED_ORIGINS → Redeploy ✅

---

## 🔑 Key Environment Variables Reference

| Variable | Where | Source |
|----------|-------|--------|
| SECRET_KEY | Render | Run `python docs/deployment/generate_secret_key.py` |
| DB_* | Render | PostgreSQL connection details |
| DEBUG | Render | Set to `False` |
| CORS_ALLOWED_ORIGINS | Render | Your Vercel frontend URL |
| REACT_APP_API_URL | Vercel | Your Render backend URL |
| REACT_APP_API_* | Vercel | Admin credentials |

---

## 🆘 Troubleshooting Quick Links

| Problem | Solution |
|---------|----------|
| "ModuleNotFoundError" | Rebuild on Render (Manual Deploy button) |
| "CORS blocked" | Update CORS_ALLOWED_ORIGINS in Render |
| "Static files 404" | Run collectstatic in build command |
| "Login fails" | Verify API_PASSWORD matches REACT_APP_API_PASSWORD |
| "Cannot connect to DB" | Check DB_* credentials |

See full troubleshooting in **docs/DEPLOYMENT.md**

---

## 💡 Pro Tips

1. **Test locally first:**
   ```bash
   # Backend
   cd chemical_visualizer
   python manage.py runserver
   
   # Frontend (new terminal)
   cd react_frontend
   npm start
   ```

2. **Use strong passwords:**
   - Don't use default `admin123`
   - Minimum 16 characters with mixed casing

3. **Monitor your deployment:**
   - Enable email notifications on Render
   - Check logs weekly for errors

4. **Plan for growth:**
   - Render free tier sleeps after 15 min inactivity
   - Upgrade to Starter ($7/month) for production
   - Vercel is free for most use cases

---

## 📞 Get Help

| Question | Where to Check |
|----------|-----------------|
| "How do I deploy?" | **docs/deployment/QUICK_DEPLOY.md** |
| "What's the checklist?" | **docs/deployment/DEPLOYMENT_CHECKLIST.md** |
| "What environment variables?" | **docs/deployment/.env.production.example** |
| "Detailed setup guide?" | **docs/DEPLOYMENT.md** |
| "Project architecture?" | **docs/PROJECT_INFO.md** |

---

## ✅ When You're Ready to Deploy

1. **Read:** docs/deployment/QUICK_DEPLOY.md (15 minutes)
2. **Prepare:** Run docs/deployment/prepare_deployment.bat/sh (2 minutes)
3. **Deploy Backend:** Render (10 minutes)
4. **Deploy Frontend:** Vercel (5 minutes)
5. **Test:** Upload CSV and verify working (5 minutes)

**Total Time: ~40 minutes for first-time deployment**

---

## 🎉 You're Ready!

Your application is now configured for professional production deployment. Just follow the docs/deployment/QUICK_DEPLOY.md guide and you'll be live in under an hour!

**Questions? Check the README or docs folder.**
