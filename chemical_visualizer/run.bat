@echo off
REM Quick Start Script for Chemical Equipment Parameter Visualizer
REM Run this script to set up and start the development server

echo ========================================
echo Chemical Equipment Parameter Visualizer
echo Django Backend Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Run migrations
echo Running database migrations...
python manage.py migrate

REM Run development server
echo.
echo ========================================
echo Starting development server...
echo Server will run at: http://localhost:8000
echo ========================================
echo.

python manage.py runserver
