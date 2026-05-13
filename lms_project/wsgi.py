"""
WSGI config for lms_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

# Load environment variables from .env file BEFORE Django initialization
try:
    from dotenv import load_dotenv
    BASE_DIR = Path(__file__).resolve().parent.parent
    env_file = BASE_DIR / '.env'
    if env_file.exists():
        load_dotenv(env_file)
except ImportError:
    pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
