"""
WSGI config untuk PythonAnywhere
Gunakan file ini sebagai WSGI configuration di tab "Web" PythonAnywhere

INSTRUKSI:
1. Ganti USERNAME dengan username PythonAnywhere Anda
2. Copy isi file ini ke WSGI configuration file di PythonAnywhere
3. Klik Reload untuk apply perubahan
"""

import os
import sys
from pathlib import Path

# PENTING: Ganti USERNAME dengan username PythonAnywhere Anda
# Contoh: jika username adalah "ammar", maka: /home/ammar/ammarpsbi
PROJECT_PATH = '/home/USERNAME/ammarpsbi'

# Tambahkan path proyek ke sys.path
if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

# Set environment variable untuk Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project.settings')

# Load environment variables dari .env file
try:
    from dotenv import load_dotenv
    env_file = Path(PROJECT_PATH) / '.env'
    if env_file.exists():
        load_dotenv(env_file)
except ImportError:
    print("Warning: python-dotenv not installed", file=sys.stderr)

# Get WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
