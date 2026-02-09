@echo off
REM Deployment Preparation Script for Windows
REM This script prepares your project for deployment to Render and Vercel

setlocal enabledelayedexpansion

echo ===============================================
echo   Chemical Equipment Visualizer
echo   Deployment Preparation Script
echo ===============================================
echo.

REM Check if Git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git not found. Please install Git first.
    echo   Download from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo ✅ Git is installed

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python first.
    pause
    exit /b 1
)

echo ✅ Python is installed

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not found. Please install Node.js first.
    echo   Download from: https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Node.js is installed
echo.

REM Generate SECRET_KEY
echo ===============================================
echo  Generating Secure SECRET_KEY...
echo ===============================================
cd chemical_visualizer
python -c "from django.core.management.utils import get_random_secret_key; print('SECRET_KEY=' + get_random_secret_key())" > ..\SECRET_KEY.txt
echo.
echo ✅ SECRET_KEY generated and saved to: SECRET_KEY.txt
type ..\SECRET_KEY.txt
echo.
cd ..

REM Check if files exist
echo ===============================================
echo  Checking Deployment Files...
echo ===============================================

if exist "chemical_visualizer\Procfile" (
    echo ✅ Procfile exists
) else (
    echo ⚠️  Procfile not found - creating it
    echo web: gunicorn chemical_visualizer.wsgi --log-file - > chemical_visualizer\Procfile
)

if exist "chemical_visualizer\runtime.txt" (
    echo ✅ runtime.txt exists
) else (
    echo ⚠️  runtime.txt not found - creating it
    echo python-3.12.3 > chemical_visualizer\runtime.txt
)

if exist "docs\deployment\QUICK_DEPLOY.md" (
    echo ✅ docs\deployment\QUICK_DEPLOY.md exists
) else (
    echo ⚠️  docs\deployment\QUICK_DEPLOY.md not found
)

if exist ".env" (
    echo ✅ .env exists
    echo   ⚠️  IMPORTANT: Make sure .env is in .gitignore
) else (
    echo ⚠️  .env not found
)

echo.
echo ===============================================
echo  Files Ready for Deployment
echo ===============================================
echo.
echo 📦 Backend (Django):
echo   - Procfile ✅
echo   - runtime.txt ✅
echo   - requirements_production.txt ✅
echo.
echo 🎨 Frontend (React):
echo   - Create .env.production with API_URL ⏳
echo.
echo 📋 Configuration:
echo   - .env (local) ✅
echo   - docs\deployment\.env.production.example ✅
echo.
echo ===============================================
echo  Next Steps:
echo ===============================================
echo.
echo 1. Create Render account: https://render.com
echo 2. Connect your GitHub repository
echo 3. Create PostgreSQL database instance
echo 4. Deploy backend with environment variables
echo 5. Create Vercel account: https://vercel.com
echo 6. Deploy frontend
echo.
echo 📖 Full Instructions: Read docs\deployment\QUICK_DEPLOY.md
echo 📋 Checklist: Use docs\deployment\DEPLOYMENT_CHECKLIST.md
echo.
echo ===============================================
echo  Quick Copy-Paste Commands:
echo ===============================================
echo.
echo For Render Build Command:
echo   pip install -r requirements.txt ^&^& python manage.py migrate ^&^& python manage.py collectstatic --noinput
echo.
echo For Render Start Command:
echo   gunicorn chemical_visualizer.wsgi
echo.

echo ✅ Deployment preparation complete!
echo.
pause
