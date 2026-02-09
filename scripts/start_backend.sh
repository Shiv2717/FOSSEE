#!/bin/bash
# Start Django API Server
echo "Starting Chemical Visualizer API Server..."
cd "$(dirname "$0")/.."
cd chemical_visualizer
source ../.venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
echo ""
echo "Starting server on http://localhost:8000"
python manage.py runserver 0.0.0.0:8000
