# API Authentication Setup

## Overview

The Django REST API now requires authentication for all endpoints:
- `/api/upload/` - POST - Upload CSV files
- `/api/history/` - GET - View upload history
- `/api/report/` - GET - Generate PDF reports

**Authentication Method:** HTTP Basic Authentication

## Setup Instructions

### 1. Apply Database Migrations

First, ensure the database has the necessary tables for user authentication:

```bash
cd chemical_visualizer
python manage.py migrate
```

### 2. Create Test User

Run the provided script to create a test user:

```bash
cd chemical_visualizer
python create_test_user.py
```

**Default Test Credentials:**
- Username: `admin`
- Password: `admin123`

### 3. Restart Django Server

If the Django server is running, restart it for changes to take effect:

```bash
python manage.py runserver
```

### 4. Update React Frontend Credentials (if needed)

Edit `react_frontend/src/App.js` and update these constants if you changed the username/password:

```javascript
const API_USERNAME = 'admin';
const API_PASSWORD = 'admin123';
```

## Testing Authentication

### Using cURL

```bash
# Upload CSV
curl -u admin:admin123 -F "csv_file=@equipment.csv" http://localhost:8000/api/upload/

# Get history
curl -u admin:admin123 http://localhost:8000/api/history/

# Generate report
curl -u admin:admin123 http://localhost:8000/api/report/ -o report.pdf
```

### Using Python requests

```python
import requests

auth = ('admin', 'admin123')

# Upload
with open('equipment.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/upload/',
        files={'csv_file': f},
        auth=auth
    )
print(response.json())

# History
response = requests.get('http://localhost:8000/api/history/', auth=auth)
print(response.json())
```

### Using React Frontend

The React app automatically includes authentication credentials with every API request. Just make sure the credentials in `App.js` match your user.

## Django Admin Access

You can also access the Django admin interface:

**URL:** http://localhost:8000/admin/

**Credentials:** Same as API (admin/admin123)

From the admin panel, you can:
- View/manage users
- View uploaded equipment data
- Change user passwords

## Creating Additional Users

### Option 1: Using Django Admin

1. Go to http://localhost:8000/admin/
2. Login with admin credentials
3. Click "Users" → "Add User"
4. Fill in username and password
5. Save

### Option 2: Using Django Shell

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User

User.objects.create_user(
    username='testuser',
    password='testpass123',
    email='test@example.com'
)
```

### Option 3: Using Management Command

```bash
python manage.py createsuperuser
```

Follow the prompts to create a new admin user.

## Security Notes

⚠️ **For Development Only**

The provided credentials (`admin/admin123`) are for **development and testing only**.

**For Production:**
1. Use strong, unique passwords
2. Enable HTTPS/TLS
3. Consider using token-based authentication (JWT)
4. Store credentials in environment variables
5. Implement rate limiting
6. Add IP whitelisting if appropriate

## Troubleshooting

### "Authentication credentials were not provided"

The API requires authentication. Make sure:
- You've created a user using `create_test_user.py`
- Your React app has the correct credentials in `App.js`
- The Authorization header is being sent with requests

### "Invalid username/password"

- Verify credentials by logging into http://localhost:8000/admin/
- Re-run `python create_test_user.py` to reset the password
- Check for typos in username/password

### "CSRF verification failed"

If using SessionAuthentication from a browser:
- Make sure CORS settings allow credentials
- Include CSRF token in requests
- BasicAuthentication doesn't require CSRF tokens

## API Response Examples

### Successful Authentication

```json
{
  "message": "CSV uploaded successfully",
  "data": {
    "id": 1,
    "filename": "equipment.csv",
    "equipment_count": 8,
    "avg_flowrate": 94.16,
    "avg_pressure": 50.73,
    "avg_temperature": 26.50
  }
}
```

### Authentication Failed (401)

```json
{
  "detail": "Authentication credentials were not provided."
}
```

Or:

```json
{
  "detail": "Invalid username/password."
}
```

## Next Steps

- Change default password after setup
- Consider implementing JWT for mobile/SPA apps
- Add user roles and permissions for multi-user scenarios
- Implement password reset functionality
- Add rate limiting to prevent brute force attacks
