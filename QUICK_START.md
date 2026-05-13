# 🚀 QUICK START: PythonAnywhere Deployment

**Waktu Setup:** ~20-30 menit (first time)

---

## 📝 Pre-Deployment (Local)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Test configuration
python verify_pythonanywhere.py

# 3. Run migrations
python manage.py migrate
python manage.py collectstatic --noinput

# 4. Test locally
python manage.py runserver
```

---

## 🔑 Update .env File

**Edit `.env` file:**
```env
DEBUG=False
SECRET_KEY=<use random key>
ALLOWED_HOSTS=localhost,127.0.0.1,USERNAME.pythonanywhere.com
```

**Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 📤 GitHub Setup

```bash
git init
git add .
git commit -m "Prepare for PythonAnywhere deployment"
git remote add origin https://github.com/USERNAME/ammarpsbi.git
git push -u origin main
```

---

## 🌐 PythonAnywhere Setup

### **1. Bash Console**
```bash
git clone https://github.com/USERNAME/ammarpsbi.git
cd ammarpsbi
mkvirtualenv --python=/usr/bin/python3.10 venv
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput --clear
```

**⚠️ PENTING:** `collectstatic` harus dijalankan atau CSS/JS tidak akan muncul!

### **2. Web Tab**
- **Virtualenv path:** `/home/USERNAME/.virtualenvs/venv`
- **Source code:** `/home/USERNAME/ammarpsbi`
- **Working directory:** `/home/USERNAME/ammarpsbi`
- **Static files:**
  - URL: `/static/`
  - Directory: `/home/USERNAME/ammarpsbi/staticfiles`

### **3. WSGI Configuration**
Replace WSGI file content with:
```python
import os
import sys
from pathlib import Path

PROJECT_PATH = '/home/USERNAME/ammarpsbi'
if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project.settings')

try:
    from dotenv import load_dotenv
    env_file = Path(PROJECT_PATH) / '.env'
    if env_file.exists():
        load_dotenv(env_file)
except ImportError:
    print("Warning: python-dotenv not installed", file=sys.stderr)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### **4. Reload**
Click **Reload** button di Web tab

---

## ✅ Check

- Access: `https://USERNAME.pythonanywhere.com`
- Check error log if needed
- Run `python verify_pythonanywhere.py` if issues

---

## 📚 Full Documentation

See **DEPLOYMENT_GUIDE.md** for complete instructions

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| 502 Bad Gateway | Check error log, run `python manage.py migrate` |
| Static files missing | Run `python manage.py collectstatic --noinput` |
| Module not found | Run `pip install -r requirements.txt` |
| Can't access site | Check ALLOWED_HOSTS in .env |

Check error log at: **Web tab → Scroll down → Error log**

---

**Status:** Ready to Deploy ✅
