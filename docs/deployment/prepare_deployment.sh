#!/bin/bash

# Deployment Preparation Script for Linux/Mac
# This script prepares your project for deployment to Render and Vercel

echo "========================================"
echo "  Chemical Equipment Visualizer"
echo "  Deployment Preparation Script"
echo "========================================"
echo ""

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install Git first."
    exit 1
fi
echo "✅ Git is installed"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi
echo "✅ Python 3 is installed"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js."
    exit 1
fi
echo "✅ Node.js is installed"
echo ""

# Generate SECRET_KEY
echo "========================================"
echo "  Generating Secure SECRET_KEY..."
echo "========================================"
cd chemical_visualizer
python3 -c "from django.core.management.utils import get_random_secret_key; print('SECRET_KEY=' + get_random_secret_key())" > ../SECRET_KEY.txt
echo ""
echo "✅ SECRET_KEY generated and saved to: SECRET_KEY.txt"
cat ../SECRET_KEY.txt
echo ""
cd ..

# Check if files exist
echo "========================================"
echo "  Checking Deployment Files..."
echo "========================================"

if [ -f "chemical_visualizer/Procfile" ]; then
    echo "✅ Procfile exists"
else
    echo "⚠️  Procfile not found - creating it"
    echo "web: gunicorn chemical_visualizer.wsgi --log-file -" > chemical_visualizer/Procfile
fi

if [ -f "chemical_visualizer/runtime.txt" ]; then
    echo "✅ runtime.txt exists"
else
    echo "⚠️  runtime.txt not found - creating it"
    echo "python-3.12.3" > chemical_visualizer/runtime.txt
fi

if [ -f "docs/deployment/QUICK_DEPLOY.md" ]; then
    echo "✅ docs/deployment/QUICK_DEPLOY.md exists"
else
    echo "⚠️  docs/deployment/QUICK_DEPLOY.md not found"
fi

if [ -f ".env" ]; then
    echo "✅ .env exists"
    echo "   ⚠️  IMPORTANT: Make sure .env is in .gitignore"
else
    echo "⚠️  .env not found"
fi

echo ""
echo "========================================"
echo "  Files Ready for Deployment"
echo "========================================"
echo ""
echo "📦 Backend (Django):"
echo "   - Procfile ✅"
echo "   - runtime.txt ✅"
echo "   - requirements_production.txt ✅"
echo ""
echo "🎨 Frontend (React):"
echo "   - Create .env.production with API_URL ⏳"
echo ""
echo "📋 Configuration:"
echo "   - .env (local) ✅"
echo "   - docs/deployment/.env.production.example ✅"
echo ""
echo "========================================"
echo "  Next Steps:"
echo "========================================"
echo ""
echo "1. Create Render account: https://render.com"
echo "2. Connect your GitHub repository"
echo "3. Create PostgreSQL database instance"
echo "4. Deploy backend with environment variables"
echo "5. Create Vercel account: https://vercel.com"
echo "6. Deploy frontend"
echo ""
echo "📖 Full Instructions: Read docs/deployment/QUICK_DEPLOY.md"
echo "📋 Checklist: Use docs/deployment/DEPLOYMENT_CHECKLIST.md"
echo ""
echo "========================================"
echo "  Quick Copy-Paste Commands:"
echo "========================================"
echo ""
echo "For Render Build Command:"
echo "   pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput"
echo ""
echo "For Render Start Command:"
echo "   gunicorn chemical_visualizer.wsgi"
echo ""
echo "✅ Deployment preparation complete!"
