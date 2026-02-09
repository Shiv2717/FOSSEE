#!/usr/bin/env python
"""
Generate a secure SECRET_KEY for Django production deployment
Run this before deploying: python docs/deployment/generate_secret_key.py
"""
from django.core.management.utils import get_random_secret_key

if __name__ == '__main__':
    print("🔐 Generated SECRET_KEY for production:")
    print("=" * 60)
    print(get_random_secret_key())
    print("=" * 60)
    print("\nCopy this to your Render environment variables:")
    print("SECRET_KEY = <paste above key>")
