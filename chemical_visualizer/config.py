"""
Configuration module for desktop application
Reads settings from environment variables or config file
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Try to load from .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    env_path = BASE_DIR / '.env'
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass

# Desktop App Configuration
DESKTOP_API_URL = os.getenv('DESKTOP_API_URL', 'http://localhost:8000')
DESKTOP_API_USERNAME = os.getenv('DESKTOP_API_USERNAME', 'admin')
DESKTOP_API_PASSWORD = os.getenv('DESKTOP_API_PASSWORD', 'admin123')

# API Endpoints
API_UPLOAD_URL = f"{DESKTOP_API_URL}/api/upload/"
API_HISTORY_URL = f"{DESKTOP_API_URL}/api/history/"
API_REPORT_URL = f"{DESKTOP_API_URL}/api/report/"
