#!/bin/bash
# Quick Start Script for Chemical Equipment Parameter Visualizer
# Run this script to set up and start the development server

echo "========================================"
echo "Chemical Equipment Parameter Visualizer"
echo "Django Backend Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Run development server
echo ""
echo "========================================"
echo "Starting development server..."
echo "Server will run at: http://localhost:8000"
echo "========================================"
echo ""

python manage.py runserver
