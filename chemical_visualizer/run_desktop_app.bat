@echo off
REM Run the PyQt5 Desktop Application
REM Make sure Django API is running first!

echo ============================================
echo Chemical Equipment Visualizer - Desktop App
echo ============================================
echo.
echo Making sure Django API is running...
echo API should be at: http://localhost:8000/api
echo.
echo Starting PyQt5 Desktop Application...
echo.

REM Activate virtual environment if it exists
if exist "..\..\.venv\Scripts\activate.bat" (
    call ..\..\..venv\Scripts\activate.bat
)

REM Run the desktop app
python desktop_app.py

pause
