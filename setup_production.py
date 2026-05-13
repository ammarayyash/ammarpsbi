#!/usr/bin/env python
"""
Script untuk setup production di PythonAnywhere
Jalankan: python setup_production.py
"""

import os
import secrets
from pathlib import Path
from dotenv import load_dotenv

# Load current .env
load_dotenv()

print("=" * 60)
print("🚀 Production Setup untuk PythonAnywhere")
print("=" * 60)

# 1. Generate new SECRET_KEY
print("\n1️⃣  Generate Secret Key...")
new_secret_key = f"django-insecure-{''.join(secrets.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for _ in range(50))}"
print(f"✅ New SECRET_KEY generated")

# 2. Get username
print("\n2️⃣  Konfigurasi ALLOWED_HOSTS...")
username = input("Masukkan username PythonAnywhere Anda: ").strip()
domain = f"{username}.pythonanywhere.com"
print(f"✅ Domain akan menggunakan: {domain}")

# 3. Update .env file
print("\n3️⃣  Update .env file...")
env_path = Path('.env')

env_content = f"""# Environment Variables untuk PythonAnywhere

# Django Settings
DEBUG=False
SECRET_KEY={new_secret_key}

# ALLOWED_HOSTS dengan domain PythonAnywhere
ALLOWED_HOSTS=localhost,127.0.0.1,{domain}

# Database (jika nanti ingin ganti ke PostgreSQL)
# DATABASE_URL=postgresql://user:password@localhost/dbname
"""

with open(env_path, 'w') as f:
    f.write(env_content)

print(f"✅ .env file sudah diupdate di {env_path}")

# 4. Show next steps
print("\n" + "=" * 60)
print("📋 Langkah Berikutnya:")
print("=" * 60)
print("""
1. Commit perubahan:
   git add .
   git commit -m "Setup production configuration for PythonAnywhere"

2. Push ke GitHub:
   git push origin main

3. Di PythonAnywhere Bash Console:
   git clone https://github.com/YOUR_USERNAME/ammarpsbi.git
   cd ammarpsbi
   mkvirtualenv --python=/usr/bin/python3.10 venv
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic --noinput

4. Setup WSGI di PythonAnywhere Web tab (lihat DEPLOYMENT_GUIDE.md)

5. Reload web app di PythonAnywhere

✨ Selesai! Akses https://{domain}
""")
