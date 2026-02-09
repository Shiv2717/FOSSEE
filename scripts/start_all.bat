@echo off
REM Start all components for development
echo Starting Chemical Visualizer - All Components
echo ============================================
echo.

cd ..

REM Start Backend in new window
start "Backend Server" cmd /k scripts\start_backend.bat

REM Wait a moment for backend to start
timeout /t 5

REM Start Frontend in new window
start "Frontend Server" cmd /k scripts\start_frontend.bat

REM Wait a moment
timeout /t 3

REM Start Desktop App in new window
start "Desktop App" cmd /k scripts\start_desktop.bat

echo.
echo All components started!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo Desktop: Running in separate window
echo.
echo Press any key to exit this window...
pause >nul
