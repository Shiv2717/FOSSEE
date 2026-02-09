#!/bin/bash
# Update all dependencies to latest versions
echo "Updating Chemical Visualizer Dependencies..."
echo "============================================"
echo ""

cd "$(dirname "$0")/.."

# Update Backend
echo "[1/3] Updating Backend Dependencies..."
cd chemical_visualizer
source ../.venv/bin/activate
pip install --upgrade -r requirements.txt
pip install --upgrade -r desktop_requirements.txt
cd ..
echo "Backend updated!"
echo ""

# Update Frontend
echo "[2/3] Updating Frontend Dependencies..."
cd react_frontend
npm update
cd ..
echo "Frontend updated!"
echo ""

# Show versions
echo "[3/3] Installed Versions:"
echo ""
echo "Python Packages:"
source .venv/bin/activate
pip list | grep -E "Django|djangorestframework|pandas|PyQt5"
echo ""
echo "Node Packages:"
cd react_frontend
npm list react axios chart.js --depth=0
cd ..
echo ""
echo "Update complete!"
