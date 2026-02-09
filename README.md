# Chemical Equipment Parameter Visualizer

A production-ready full-stack application for uploading, analyzing, and visualizing chemical equipment parameters from CSV files. Built with Django REST Framework backend, React.js frontend, and PyQt5 desktop client.

## 🎯 Project Overview

This application allows users to upload CSV files containing chemical equipment data (flow rate, pressure, temperature) and provides:
- Statistical analysis (averages, counts, type distribution)
- Interactive visualizations (bar charts, pie charts)
- PDF report generation
- RESTful API with authentication
- Multi-platform access (Web + Desktop)
- **Production-ready with environment-based configuration**
- **Real data support with no test data dependencies**

**Developed for:** Chemical Engineering Data Management  
**Purpose:** Internship Project / Portfolio Demonstration

---

## 🚀 Quick Start (Production Ready)

### One-Click Start (All Components)
```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

### Manual Start (Individual Components)
```bash
# Windows
scripts\start_backend.bat       # API Server
scripts\start_frontend.bat      # Web App
scripts\start_desktop.bat       # Desktop App

# Linux/Mac
./scripts/start_backend.sh &
./scripts/start_frontend.sh &
```

### Production Deployment
```bash
# Windows
scripts\start_production.bat

# Linux/Mac
./scripts/start_production.sh
```

**📚 For detailed instructions, see [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)**

---

## 🛠️ Tech Stack

### Backend
- **Django 4.2.7** - Web framework
- **Django REST Framework** - REST API
- **pandas** - Data processing
- **ReportLab** - PDF generation
- **SQLite** - Database

### Web Frontend
- **React 18.2** - UI library
- **Axios** - HTTP client
- **Chart.js** - Data visualization
- **React-Chart.js-2** - React wrapper for Chart.js

### Desktop Application
- **PyQt5** - GUI framework
- **Requests** - API client

---

## 📁 Project Structure

```
FOSSENN/
├── 📄 README.md              # Main documentation
├── 📄 LICENSE                # MIT License
├── 🔧 .env.example           # Environment template
├── 🚀 start.bat / start.sh   # Quick start launcher
├── 
├── 📁 chemical_visualizer/   # Django Backend
│   ├── manage.py
│   ├── desktop_app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── equipment_api/        # API application
│   └── ...
├── 
├── 📁 react_frontend/        # React Web App
│   ├── package.json
│   ├── src/
│   │   ├── App.js
│   │   └── ...
│   └── ...
├── 
├── 📁 scripts/               # All startup & build scripts
│   ├── start_backend.*
│   ├── start_frontend.*
│   ├── start_desktop.*
│   ├── start_production.*
│   ├── build_frontend.*
│   └── update_dependencies.*
├── 
└── 📁 docs/                  # Documentation
    ├── DEPLOYMENT.md         # Complete deployment guide
    ├── SETUP.md              # Quick setup guide
    ├── QUICK_REFERENCE.md    # Command reference
    └── PROJECT_INFO.md       # Project details
```

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+ and npm
- Git

### 1️⃣ Backend Setup (Django API)

```bash
# Navigate to project directory
cd chemical_visualizer

# Install Python dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Create admin user (username: admin, password: admin123)
python create_test_user.py

# Start Django development server
python manage.py runserver
```

**Backend will run on:** http://localhost:8000

### 2️⃣ Web Frontend Setup (React)

```bash
# Navigate to React directory
cd react_frontend

# Install Node dependencies
npm install

# Start development server
npm start
```

**Frontend will run on:** http://localhost:3000

### 3️⃣ Desktop App Setup (PyQt5)

```bash
# Navigate to backend directory
cd chemical_visualizer

# Install desktop dependencies
pip install PyQt5 requests

# Run desktop application
python desktop_app.py
```

---

## 🔐 Authentication

All API endpoints require **HTTP Basic Authentication**.

**Default Credentials:**
- Username: `admin`
- Password: `admin123`

The React app and desktop app automatically include these credentials. Change them in production environments.

---

## 📡 API Endpoints

### Base URL: `http://localhost:8000/api`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/upload/` | Upload CSV file and get analysis | ✓ |
| GET | `/history/` | Get last 5 uploads | ✓ |
| GET | `/report/?upload_id={id}` | Generate PDF report | ✓ |

### Upload Response Example

```json
{
  "message": "CSV uploaded successfully",
  "data": {
    "id": 1,
    "filename": "equipment.csv",
    "equipment_count": 8,
    "avg_flowrate": 94.16,
    "avg_pressure": 50.73,
    "avg_temperature": 26.50,
    "type_distribution": {
      "Centrifugal": 2,
      "Reciprocating": 1,
      "Rotary": 1
    },
    "equipment": [
      {
        "name": "Pump A",
        "type": "Centrifugal",
        "flowrate": 100.5,
        "pressure": 50.2,
        "temperature": 25.1
      }
    ]
  }
}
```

---

## 📊 CSV File Format

Your CSV file must contain these columns:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump A,Centrifugal,100.5,50.2,25.1
Pump B,Reciprocating,85.3,45.8,26.5
Compressor X,Rotary,120.0,60.5,30.2
```

**Sample file:** `test_equipment.csv` is included in the project

---

## 🎬 Demo Instructions

### Quick Start - All Services

1. **Terminal 1 - Django Backend:**
   ```bash
   cd chemical_visualizer
   python manage.py runserver
   ```

2. **Terminal 2 - React Frontend:**
   ```bash
   cd react_frontend
   npm start
   ```

3. **Browser:** Opens automatically at http://localhost:3000

4. **Upload Test File:**
   - Click "Choose CSV file"
   - Select `test_equipment.csv`
   - Click "Upload & Analyze"
   - View charts and statistics

### Desktop App Demo

```bash
cd chemical_visualizer
python desktop_app.py
```
- Click "Browse..." → Select CSV
- Click "Upload & Analyze"
- View statistics and details

### Django Admin Panel

- URL: http://localhost:8000/admin/
- Login: admin / admin123
- View uploaded data and manage users

---

## ✨ Key Features

### Web Application
✅ CSV file upload with drag & drop  
✅ Real-time data validation  
✅ Interactive bar charts (average metrics)  
✅ Pie charts (equipment type distribution)  
✅ Responsive design (mobile-friendly)  
✅ Upload history tracking  
✅ Equipment data table view  

### Desktop Application
✅ Native PyQt5 GUI  
✅ Non-blocking file upload  
✅ Statistics display panel  
✅ Detailed results viewer  
✅ Error handling with dialogs  
✅ Structured for future chart integration  

### Backend API
✅ RESTful API design  
✅ Basic authentication  
✅ CSV parsing with pandas  
✅ Statistical analysis  
✅ PDF report generation  
✅ CORS support  
✅ Comprehensive error handling  

---

## 🧪 Testing

### Test API with cURL

```bash
# Upload CSV
curl -u admin:admin123 \
  -F "csv_file=@test_equipment.csv" \
  http://localhost:8000/api/upload/

# Get history
curl -u admin:admin123 \
  http://localhost:8000/api/history/

# Download PDF report
curl -u admin:admin123 \
  http://localhost:8000/api/report/ \
  -o report.pdf
```

### Test with Python

```python
import requests

auth = ('admin', 'admin123')

# Upload
with open('test_equipment.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/upload/',
        files={'csv_file': f},
        auth=auth
    )
    print(response.json())
```

---

## 📸 Screenshots

### Web Application
- **Upload Interface:** Clean file selection with upload button
- **Statistics Cards:** Total count, equipment types, averages
- **Bar Chart:** Visual comparison of average metrics
- **Pie Chart:** Equipment type distribution
- **Data Table:** Detailed equipment listing

### Desktop Application
- **Main Window:** Professional PyQt5 interface
- **Upload Section:** File browser and upload controls
- **Statistics Panel:** Real-time data display
- **Details View:** Scrollable text area with formatted results

---

## 🏭 Production Deployment

### Environment Configuration

This application is **production-ready** with environment-based configuration:

**Step 1: Copy environment templates**
```bash
# Backend
cp chemical_visualizer/.env.example chemical_visualizer/.env

# Frontend
cp react_frontend/.env.example react_frontend/.env
```

**Step 2: Update critical settings in `.env` files**
```env
# Backend: chemical_visualizer/.env
SECRET_KEY=generate-a-long-random-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,your-server-ip
API_USERNAME=your_admin
API_PASSWORD=strong-secure-password

# Frontend: react_frontend/.env
REACT_APP_API_URL=https://your-api-domain.com
REACT_APP_API_USERNAME=your_admin
REACT_APP_API_PASSWORD=strong-secure-password
```

### Quick Production Start

**All Components (Development):**
```bash
# Windows
start_all.bat

# Linux/Mac
./start_backend.sh &
./start_frontend.sh &
./start_desktop.sh &
```

**Production Server (Gunicorn/Waitress):**
```bash
# Windows
start_production.bat

# Linux/Mac
./start_production.sh
```

### Real Data Usage

**No test data required!** This application is ready for production data:

1. **CSV Format Requirements:**
   - `equipment_id` - Unique identifier
   - `equipment_type` - Type of equipment
   - `flowrate`, `pressure`, `temperature` - Numeric values
   - `timestamp` - Date/time of measurement

2. **Upload Methods:**
   - Web interface (http://your-domain:3000)
   - Desktop application
   - Direct API calls with curl/scripts

3. **Automatic Admin Creation:**
   - Production scripts automatically create admin user
   - Change default credentials in `.env` files

### Deployment Options

- **Local Network:** Update IP addresses in `.env` files
- **Cloud (AWS, DigitalOcean):** Use production scripts with Nginx/Apache
- **Windows Service:** Use NSSM for background operation
- **Docker:** See `DEPLOYMENT.md` for containerization options

**📚 For comprehensive deployment guide, see [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)**

---

## 🔧 Troubleshooting

### Backend Issues

**"Module not found" errors:**
```bash
pip install -r requirements.txt
```

**"Authentication credentials were not provided":**
```bash
python create_test_user.py
```

### Frontend Issues

**Port 3000 already in use:**
```bash
# Kill process or use different port
npm start -- --port 3001
```

**CORS errors:**
- Ensure Django server is running
- Check CORS settings in `settings.py`

### Desktop App Issues

**PyQt5 import error:**
```bash
pip install PyQt5
```

**Connection error:**
- Verify Django server is running on port 8000
- Check firewall settings

---

## 📦 Dependencies

### Backend (Python)
```
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
pandas==2.1.3
openpyxl==3.10.10
reportlab==4.0.7
PyQt5>=5.15.0
requests>=2.31.0
```

### Frontend (Node.js)
```
react: ^18.2.0
axios: ^1.6.0
chart.js: ^4.4.0
react-chartjs-2: ^5.2.0
```

---

## 🎓 Learning Outcomes

This project demonstrates:
- Full-stack development skills
- RESTful API design and implementation
- Frontend framework proficiency (React)
- Desktop application development (PyQt5)
- Database modeling and ORM usage
- Authentication and security
- Data processing with pandas
- Data visualization techniques
- Cross-platform development
- Version control with Git

---

## 👤 Author

**Developer:** [Your Name]  
**Email:** [your.email@example.com]  
**LinkedIn:** [Your LinkedIn Profile]  
**GitHub:** [Your GitHub Profile]

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- Django REST Framework documentation
- React.js community
- Chart.js library
- PyQt5 tutorials
- Stack Overflow community

---

## 📞 Contact & Support

For questions or support:
- Open an issue on GitHub
- Email: [your.email@example.com]
- Documentation: See individual README files in subdirectories

---

**⭐ If you found this project helpful, please consider giving it a star!**

---

*Last Updated: February 2026*
