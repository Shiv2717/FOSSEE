# 🚀 Quick Deployment Guide - After GitHub Upload

## 📋 Complete Deployment Workflow

This guide takes you through deploying to production in 3 parts:
1. **Backend** → Render.com (free tier available)
2. **Frontend** → Vercel (free tier available)  
3. **Desktop App** → Distribute as standalone executable

---

## Part 1️⃣: Deploy Backend to Render

### Step 1: Prepare Your Repository
Your GitHub repo should have this structure:
```
FOSSENN/
├── chemical_visualizer/       ← Django backend
├── react_frontend/            ← React frontend
├── docs/
│   └── deployment/
│       ├── QUICK_DEPLOY.md
│       ├── DEPLOYMENT_CHECKLIST.md
│       ├── DEPLOYMENT_GUIDE.md
│       ├── .env.production.example
│       ├── prepare_deployment.bat
│       ├── prepare_deployment.sh
│       └── generate_secret_key.py
├── scripts/
├── .env                        ← Configuration
├── README.md
└── requirements.txt           ← Backend dependencies
```

### Step 2: Prepare Backend for Deployment

1. **Update [/chemical_visualizer/requirements.txt](/chemical_visualizer/requirements.txt) with production server:**

   Add these lines:
   ```
   gunicorn==21.2.0
   python-decouple==3.8
   psycopg2-binary==2.9.9
   whitenoise==6.5.0
   ```

2. **Create [/chemical_visualizer/runtime.txt](/chemical_visualizer/runtime.txt):**
   ```
   python-3.12.3
   ```

3. **Create [/chemical_visualizer/Procfile](/chemical_visualizer/Procfile):**
   ```
   web: gunicorn chemical_visualizer.wsgi --log-file -
   ```

4. **Update [/chemical_visualizer/chemical_visualizer/settings.py](/chemical_visualizer/chemical_visualizer/settings.py):**

   Find the ALLOWED_HOSTS line and update:
   ```python
   # OLD
   ALLOWED_HOSTS = str(os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1')).split(',')
   
   # NEW - Add your Render domain
   ALLOWED_HOSTS = [
       'localhost',
       '127.0.0.1',
       'your-app-name.onrender.com',  # Replace with your Render domain
   ]
   ```

   Add/Update STATIC files at the end of settings.py:
   ```python
   STATIC_URL = '/static/'
   STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
   ```

### Step 3: Create Render Deployment

1. Go to **[render.com](https://render.com)** → Sign up → Connect GitHub
2. Click **"New +"** → **"Web Service"**
3. Select your **FOSSENN** repository
4. Fill in details:
   - **Name:** `chemical-visualizer-backend`
   - **Root Directory:** `chemical_visualizer`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start Command:** `gunicorn chemical_visualizer.wsgi`

5. Click **"Advanced"** → Add Environment Variables:
   ```
   DEBUG = False
   SECRET_KEY = <generate-new-secret-key>
   ALLOWED_HOSTS = your-app-name.onrender.com
   DB_ENGINE = django.db.backends.postgresql
   DB_NAME = <your_db_name>
   DB_USER = <your_db_user>
   DB_PASSWORD = <your_db_password>
   DB_HOST = <your_db_host>
   CSRF_TRUSTED_ORIGINS = https://your-app-name.onrender.com,https://your-frontend-domain.vercel.app
   ```

6. Click **"Create Web Service"** → Wait for deployment ✅

**Your backend is now live at:** `https://your-app-name.onrender.com`

---

## Part 2️⃣: Deploy Frontend to Vercel

### Step 1: Prepare Frontend

1. **Update [/react_frontend/.env.production](/react_frontend/.env.production):**
   ```
   REACT_APP_API_URL=https://your-app-name.onrender.com
   REACT_APP_API_USERNAME=admin
   REACT_APP_API_PASSWORD=your_api_password
   ```

2. **Update [/react_frontend/src/App.js](/react_frontend/src/App.js)** to use production URL:
   ```javascript
   const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
   ```

### Step 2: Deploy to Vercel

1. Go to **[vercel.com](https://vercel.com)** → Sign up → Connect GitHub
2. Click **"New Project"**
3. Import **FOSSENN** repository
4. Configure:
   - **Framework:** React
   - **Root Directory:** `react_frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `build`

5. Add Environment Variables:
   ```
   REACT_APP_API_URL = https://your-app-name.onrender.com
   REACT_APP_API_USERNAME = admin
   REACT_APP_API_PASSWORD = your_api_password
   ```

6. Click **"Deploy"** → Wait for deployment ✅

**Your frontend is now live at:** `https://your-app-name.vercel.app`

---

## Part 3️⃣: Update Backend CORS for Frontend

After deploying frontend, update Render environment variables:

1. Go to **Render Dashboard** → Your Service → **Environment**
2. Update `CORS_ALLOWED_ORIGINS`:
   ```
   https://your-app-name.vercel.app,http://localhost:3000,http://localhost:3002
   ```

3. Click **"Save"** → Service will redeploy automatically

---

## Part 4️⃣: Distribute Desktop App (Optional)

### Option A: PyInstaller (Easiest)

```bash
# 1. Install PyInstaller
pip install pyinstaller

# 2. Create executable
cd chemical_visualizer
pyinstaller --onefile --windowed desktop_app.py

# 3. Executable is in: ./dist/desktop_app.exe
# 4. Share this .exe file (works on Windows without Python installed)
```

### Option B: GitHub Releases

1. Build executable (see Option A above)
2. Go to GitHub → **Releases** → **Create New Release**
3. Upload `desktop_app.exe` as an asset
4. Users download and run directly

---

## 🔗 Testing After Deployment

### 1. Test Backend API
```bash
curl -X GET https://your-app-name.onrender.com/api/ \
  -H "Authorization: Basic $(echo -n 'admin:password' | base64)"
```

### 2. Test Frontend
- Open `https://your-app-name.vercel.app`
- Login with `admin / your_api_password`
- Try uploading test CSV

### 3. Test Desktop App
- Update `.env` in desktop_app folder to use Render URL:
  ```
  DESKTOP_API_URL=https://your-app-name.onrender.com
  ```
- Run desktop app and test upload

---

## 📊 Production Checklist

- [ ] Backend deployed to Render
- [ ] Frontend deployed to Vercel
- [ ] Environment variables configured
- [ ] CORS settings updated
- [ ] Database backup plan in place
- [ ] SSL certificates active (automatic)
- [ ] Tested login and file upload
- [ ] Desktop app executable created and tested

---

## 💰 Cost Estimate (Free Tier)

| Service | Plan | Cost |
|---------|------|------|
| Render | Starter | Free (with limitations) |
| Vercel | Hobby | Free |
| GitHub | Public repo | Free |
| **Total** | | **Free** |

⚠️ Render free tier sleeps after 15 mins inactivity. Upgrade to Starter plan ($7/month) for production.

---

## 🆘 Common Issues

### "Import Error: No module named 'django'"
Solution: Rebuild on Render. Go to Dashboard → Service → **Manual Deploy**

### "CORS error - blocked by CORS policy"
Solution: Update `CORS_ALLOWED_ORIGINS` in Render environment variables

### "Static files not loading"
Solution: Run `python manage.py collectstatic` in build command

### "Database connection error"
Solution: Verify `DB_*` credentials match your database service

---

## 📝 Environment Variables Map

### Backend (Render)
```
DEBUG = False
SECRET_KEY = django-insecure-xxxxx...
ALLOWED_HOSTS = your-app-name.onrender.com
DB_ENGINE = django.db.backends.postgresql
DB_NAME = database_name
DB_USER = username
DB_PASSWORD = password
DB_HOST = hostname.onrender.com
CSRF_TRUSTED_ORIGINS = https://your-frontend.vercel.app
CORS_ALLOWED_ORIGINS = https://your-frontend.vercel.app
API_USERNAME = admin
API_PASSWORD = your_secure_password
```

### Frontend (Vercel)
```
REACT_APP_API_URL = https://your-app-name.onrender.com
REACT_APP_API_USERNAME = admin
REACT_APP_API_PASSWORD = your_api_password
```

---

## 🔐 Security Best Practices

1. **Never commit .env files** - Use `.gitignore`
2. **Change default credentials** before deploying
3. **Use strong SECRET_KEY** - Generate with: `python docs/deployment/generate_secret_key.py`
4. **Enable DEBUG=False** in production
5. **Use HTTPS** (automatic on Render/Vercel)
6. **Rotate API passwords** regularly

---

## 📞 Support URLs

- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs
- Django Deployment: https://docs.djangoproject.com/en/6.0/howto/deployment/
- React Deployment: https://create-react-app.dev/deployment/

---

**Ready to deploy? Start with Part 1️⃣!**
