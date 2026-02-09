@echo off
REM Production start script for Django API with Gunicorn
echo Starting Chemical Visualizer API Server (Production Mode)...
cd %~dp0..
cd chemical_visualizer
call ..\.venv\Scripts\activate.bat

REM Apply migrations
python manage.py migrate

REM Collect static files
python manage.py collectstatic --noinput

REM Create superuser if it doesn't exist (production ready)
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"

echo.
echo Starting production server with Waitress on http://localhost:8000
echo Press CTRL+C to stop the server
waitress-serve --port=8000 chemical_visualizer.wsgi:application
