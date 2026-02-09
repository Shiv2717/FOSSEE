#!/bin/bash
# Start PyQt5 Desktop Application
echo "Starting Chemical Visualizer Desktop App..."
cd "$(dirname "$0")/.."
cd chemical_visualizer
source ../.venv/bin/activate
python desktop_app.py
