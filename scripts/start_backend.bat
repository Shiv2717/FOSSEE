@echo off
REM Start Django API Server
echo.
echo ╔════════════════════════════════════════════════╗
echo ║  Starting Chemical Visualizer API Server...    ║
echo ╚════════════════════════════════════════════════╝
echo.

cd %~dp0..
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

cd chemical_visualizer
call ..\.venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt -q

echo Running migrations...
python manage.py migrate

echo Collecting static files...
python manage.py collectstatic --noinput -q

echo.
echo ✅ Starting Django server on http://localhost:8000
echo Press Ctrl+C to stop
echo.

python manage.py runserver 0.0.0.0:8000
