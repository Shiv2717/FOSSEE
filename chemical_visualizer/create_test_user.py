"""
Create a test user for API authentication.

Run this script from the chemical_visualizer directory:
    python create_test_user.py

Default credentials:
    Username: admin
    Password: admin123
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chemical_visualizer.settings')
django.setup()

from django.contrib.auth.models import User

def create_test_user():
    """Create a test user with admin credentials."""
    username = 'admin'
    password = 'admin123'
    email = 'admin@example.com'
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        print(f"✓ User '{username}' already exists")
        user = User.objects.get(username=username)
        # Update password in case it changed
        user.set_password(password)
        user.save()
        print(f"✓ Password updated for user '{username}'")
    else:
        # Create new user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True
        )
        print(f"✓ Created new user: '{username}'")
    
    print("\n" + "="*50)
    print("TEST USER CREDENTIALS")
    print("="*50)
    print(f"Username: {username}")
    print(f"Password: {password}")
    print("="*50)
    print("\nUse these credentials to:")
    print("1. Login to Django admin: http://localhost:8000/admin/")
    print("2. Authenticate API requests from React app")
    print("="*50)

if __name__ == '__main__':
    try:
        create_test_user()
    except Exception as e:
        print(f"❌ Error creating user: {e}")
