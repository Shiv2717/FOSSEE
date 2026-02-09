@echo off
setlocal enabledelayedexpansion

REM ============================================================================
REM Chemical Visualizer - Complete Deployment Launcher
REM ============================================================================
REM This script starts all components: Django Backend, React Frontend, Desktop App
REM ============================================================================

cls
echo.
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                  🚀 CHEMICAL VISUALIZER - AUTO LAUNCHER                    ║
echo ║                         Starting All Components...                         ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.

REM Check if .venv exists
if not exist ".venv" (
    echo ❌ Virtual environment not found!
    echo Creating Python virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo 📦 Activating Python environment...
call .venv\Scripts\activate.bat

REM Install/upgrade pip
python -m pip install --upgrade pip -q

REM Install backend dependencies
echo 📦 Installing backend dependencies...
cd chemical_visualizer
if exist "requirements.txt" (
    pip install -r requirements.txt -q
    if errorlevel 1 (
        echo ⚠️  Warning: Some dependencies may not have installed
    )
)
cd ..

REM Install frontend dependencies
echo 📦 Installing frontend dependencies...
cd react_frontend
if not exist "node_modules" (
    echo Installing npm packages...
    call npm install -q
)
cd ..

REM Clear any old processes on ports
echo 🔄 Clearing old processes...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im node.exe >nul 2>&1
timeout /t 2 >nul

REM Start Backend
echo.
echo 🔧 Starting Django Backend...
start "Chemical Visualizer - Backend (Port 8000)" cmd /k ^
    "cd chemical_visualizer && ..\\.venv\\Scripts\\activate.bat && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"

REM Wait for backend to initialize
timeout /t 5 >nul

REM Start Frontend
echo 🎨 Starting React Frontend...
start "Chemical Visualizer - Frontend (Port 3002)" cmd /k ^
    "cd react_frontend && ..\\node_modules\\.bin\\react-scripts.cmd start --port 3002"

REM Wait for frontend to start
timeout /t 8 >nul

REM Start Desktop App (optional)
echo 💻 Starting Desktop Application...
if exist "chemical_visualizer\desktop_requirements.txt" (
    start "Chemical Visualizer - Desktop App" cmd /k ^
        "cd chemical_visualizer && ..\\.venv\\Scripts\\python.exe desktop_app.py"
)

echo.
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                     ✅ ALL COMPONENTS STARTED!                            ║
echo ╠════════════════════════════════════════════════════════════════════════════╣
echo ║  🌐 Frontend:  http://localhost:3002                                       ║
echo ║  🔧 Backend:   http://localhost:8000                                       ║
echo ║  🔐 Admin:     http://localhost:8000/admin                                 ║
echo ║  📡 API:       http://localhost:8000/api                                   ║
echo ║                                                                            ║
echo ║  Login Credentials:                                                       ║
echo ║  Username: admin                                                          ║
echo ║  Password: admin123                                                       ║
echo ║                                                                            ║
echo ║  📁 Test File: chemical_visualizer\test_equipment.csv                      ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.
echo ⏳ Opening browser in 5 seconds...
timeout /t 5 >nul

REM Open browser to React frontend
start http://localhost:3002

echo ✅ Done! All services are running.
echo 📝 Close these windows to stop the services.
pause
