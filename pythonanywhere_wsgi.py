"""
WSGI config untuk PythonAnywhere
Gunakan file ini sebagai WSGI configuration di tab "Web" PythonAnywhere
"""

import os
import sys
from pathlib import Path

# Tambahkan path proyek ke sys.path
# GANTI /home/username/ammarpsbi dengan path actual Anda di PythonAnywhere
project_path = '/home/USERNAME/ammarpsbi'
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# Set environment variable untuk Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project.settings')

# Load environment variables dari .env file
from pathlib import Path
import dotenv

env_file = Path(project_path) / '.env'
dotenv.load_dotenv(env_file)

# Get WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
