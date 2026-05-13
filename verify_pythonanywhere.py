#!/usr/bin/env python
"""
Script untuk verify konfigurasi PythonAnywhere sebelum deploy
Jalankan: python verify_pythonanywhere.py
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project.settings')

# Add project to path
project_path = Path(__file__).resolve().parent
sys.path.insert(0, str(project_path))

# Setup Django
django.setup()

from django.conf import settings

print("=" * 70)
print("🔍 VERIFICATION: PythonAnywhere Configuration")
print("=" * 70)

# 1. Check DEBUG mode
print("\n1️⃣  DEBUG Mode:")
print(f"   DEBUG = {settings.DEBUG}")
if settings.DEBUG:
    print("   ⚠️  WARNING: DEBUG=True! Set DEBUG=False in .env untuk production!")
else:
    print("   ✅ DEBUG=False (Production mode)")

# 2. Check SECRET_KEY
print("\n2️⃣  SECRET_KEY:")
secret_key = settings.SECRET_KEY
if 'insecure' in secret_key.lower():
    print(f"   ⚠️  WARNING: Using insecure SECRET_KEY!")
    print("      Generate new key with: python manage.py shell")
    print("      >>> from django.core.management.utils import get_random_secret_key")
    print("      >>> print(get_random_secret_key())")
else:
    print("   ✅ Secure SECRET_KEY configured")

# 3. Check ALLOWED_HOSTS
print("\n3️⃣  ALLOWED_HOSTS:")
for host in settings.ALLOWED_HOSTS:
    print(f"   - {host}")
if '*' in settings.ALLOWED_HOSTS:
    print("   ⚠️  WARNING: Using wildcard '*' in ALLOWED_HOSTS!")
    print("      Configure specific domain for PythonAnywhere!")
else:
    print("   ✅ ALLOWED_HOSTS properly configured")

# 4. Check Static Files
print("\n4️⃣  Static Files Configuration:")
print(f"   STATIC_URL = {settings.STATIC_URL}")
print(f"   STATIC_ROOT = {settings.STATIC_ROOT}")
print(f"   STATICFILES_STORAGE = {settings.STATICFILES_STORAGE}")
if 'whitenoise' in settings.STATICFILES_STORAGE.lower():
    print("   ✅ WhiteNoise configured for static files")
else:
    print("   ⚠️  WARNING: WhiteNoise not configured!")

# 5. Check Media Files
print("\n5️⃣  Media Files Configuration:")
print(f"   MEDIA_URL = {settings.MEDIA_URL}")
print(f"   MEDIA_ROOT = {settings.MEDIA_ROOT}")
print("   ✅ Media files configured")

# 6. Check Middleware
print("\n6️⃣  Middleware:")
has_whitenoise = any('whitenoise' in mw.lower() for mw in settings.MIDDLEWARE)
has_security = any('security' in mw.lower() for mw in settings.MIDDLEWARE)
if has_whitenoise:
    print("   ✅ WhiteNoise middleware present")
else:
    print("   ⚠️  WARNING: WhiteNoise middleware not found!")
if has_security:
    print("   ✅ Security middleware present")
else:
    print("   ⚠️  WARNING: Security middleware not found!")

# 7. Check Installed Apps
print("\n7️⃣  Installed Apps:")
required_apps = ['django.contrib.staticfiles', 'rest_framework', 'dashboard']
for app in required_apps:
    if app in settings.INSTALLED_APPS:
        print(f"   ✅ {app}")
    else:
        print(f"   ⚠️  {app} NOT FOUND!")

# 8. Check Security Settings
print("\n8️⃣  Security Settings (Production):")
if not settings.DEBUG:
    checks = {
        'CSRF_COOKIE_SECURE': getattr(settings, 'CSRF_COOKIE_SECURE', False),
        'SESSION_COOKIE_SECURE': getattr(settings, 'SESSION_COOKIE_SECURE', False),
        'SECURE_HSTS_SECONDS': getattr(settings, 'SECURE_HSTS_SECONDS', 0),
    }
    for check, value in checks.items():
        if value:
            print(f"   ✅ {check} = {value}")
        else:
            print(f"   ⚠️  {check} not configured")
else:
    print("   ⏭️  Security settings only active in production (DEBUG=False)")

# 9. Check WSGI
print("\n9️⃣  WSGI Configuration:")
print(f"   WSGI_APPLICATION = {settings.WSGI_APPLICATION}")
print("   ✅ WSGI configured")

# 10. Summary
print("\n" + "=" * 70)
print("📝 SUMMARY:")
print("=" * 70)

checks_passed = [
    not settings.DEBUG,
    'insecure' not in settings.SECRET_KEY.lower(),
    '*' not in settings.ALLOWED_HOSTS,
    has_whitenoise,
]

passed = sum(checks_passed)
total = len(checks_passed)

print(f"Checks passed: {passed}/{total}")

if passed == total:
    print("\n✅ Configuration looks GOOD! Ready for deployment.")
else:
    print(f"\n⚠️  {total - passed} issue(s) found. Please fix before deployment.")

print("=" * 70)
