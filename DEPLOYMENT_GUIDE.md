# 🚀 Panduan Deployment ke PythonAnywhere (UPDATED v2)

Panduan lengkap untuk mendeploy project `ammarpsbi` ke PythonAnywhere dengan konfigurasi production-ready.

---

## ✅ Pre-Deployment Checklist

Sebelum mulai, pastikan:
- [ ] File `.env` sudah dibuat
- [ ] `requirements.txt` sudah diupdate
- [ ] `settings.py` sudah dikonfigurasi
- [ ] Jalankan `python verify_pythonanywhere.py` untuk check konfigurasi

---

## 🔧 Langkah-Langkah Deployment

### **Step 1: Verify Konfigurasi Lokal**

Pertama, test konfigurasi Anda secara lokal:

```bash
# Install dependensi terlebih dahulu
pip install -r requirements.txt

# Verify konfigurasi
python verify_pythonanywhere.py

# Jika semua OK, jalankan
python manage.py migrate
python manage.py collectstatic --noinput
```

### **Step 2: Update .env File**

Edit file `.env` dan sesuaikan dengan username PythonAnywhere Anda:

```env
DEBUG=False
SECRET_KEY=your-generated-random-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,USERNAME.pythonanywhere.com
```

**Untuk generate SECRET_KEY yang aman:**
```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
```

### **Step 3: Setup Git Repository**

```bash
# Initialize git (jika belum ada)
git init

# Add all files
git add .

# Commit
git commit -m "Prepare for PythonAnywhere deployment"

# Add remote (ganti USERNAME dengan GitHub username Anda)
git remote add origin https://github.com/USERNAME/ammarpsbi.git

# Push
git branch -M main
git push -u origin main
```

---

## 🌐 Setup di PythonAnywhere

### **Step 4: Clone Repository di PythonAnywhere**

1. Login ke https://www.pythonanywhere.com
2. Buka **Bash Console** dari menu
3. Jalankan:

```bash
# Clone repository
git clone https://github.com/USERNAME/ammarpsbi.git
cd ammarpsbi

# Create virtual environment
mkvirtualenv --python=/usr/bin/python3.10 venv

# Install dependencies
pip install -r requirements.txt
```

### **Step 5: Setup Database & Static Files**

```bash
# Migrate database
python manage.py migrate

# Collect static files (VERY IMPORTANT!)
python manage.py collectstatic --noinput --clear
```

**⚠️ PENTING:** Step `collectstatic` ini HARUS dijalankan, atau CSS/JavaScript tidak akan muncul!

### **Step 6: Configure Web App**

1. Go ke tab **Web** di PythonAnywhere dashboard
2. Klik **"Add a new web app"**
3. Pilih **"Manual configuration"** → **Python 3.10**

**Configure Virtual Environment:**
- Di field "Virtualenv path", masukkan: `/home/USERNAME/.virtualenvs/venv`

**Configure Source Code:**
- Source code: `/home/USERNAME/ammarpsbi`
- Working directory: `/home/USERNAME/ammarpsbi`

**Configure Static Files:**
- URL: `/static/`
- Directory: `/home/USERNAME/ammarpsbi/staticfiles`

### **Step 7: Edit WSGI Configuration File**

1. Di tab **Web**, scroll ke bawah
2. Klik link ke WSGI configuration file (biasanya ada di section "Code")
3. **Hapus semua** isi file yang ada
4. Paste kode ini (GANTI USERNAME):

```python
import os
import sys
from pathlib import Path

# GANTI USERNAME dengan username PythonAnywhere Anda
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

5. Klik **Save**

### **Step 8: Reload Web App**

1. Scroll ke atas di tab **Web**
2. Klik tombol **Reload** (warna hijau)
3. Tunggu status berubah ke "Running"

---

## ✨ Testing Deployment

Setelah reload, akses website Anda:
```
https://USERNAME.pythonanywhere.com
```

### **Jika muncul halaman login/dashboard:**
✅ **Deployment BERHASIL!**

### **Jika ada error:**

1. **Cek Error Log:**
   - Tab Web → Scroll ke bawah → "Error log"
   - Copy error message untuk debugging

2. **Common Errors & Solutions:**

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'dotenv'` | `pip install python-dotenv` |
| `No such file or directory: '.env'` | Pastikan .env file sudah di `/home/USERNAME/ammarpsbi/` |
| `SyntaxError` di WSGI file | Cek indentation, copas ulang dari template |
| `502 Bad Gateway` | Jalankan `python manage.py migrate` lagi |
| Static files tidak muncul | Jalankan `python manage.py collectstatic --noinput` |

3. **Debugging via Bash Console:**

```bash
cd /home/USERNAME/ammarpsbi

# Test konfigurasi
python verify_pythonanywhere.py

# Check .env file
cat .env

# Check Django settings
python manage.py shell
>>> from django.conf import settings
>>> print(settings.DEBUG)
>>> print(settings.ALLOWED_HOSTS)
```

---

## 🔄 Update Code di Production

Setiap kali ada perubahan:

```bash
# 1. Local: Push ke GitHub
git add .
git commit -m "Your message"
git push origin main

# 2. PythonAnywhere Bash Console
cd /home/USERNAME/ammarpsbi
git pull origin main

# 3. Jika ada perubahan database/static
python manage.py migrate
python manage.py collectstatic --noinput

# 4. Reload di Web tab
```

---

## 🔐 Production Security Checklist

✅ Sudah dikonfigurasi:
- `DEBUG = False` (dari .env)
- `CSRF_COOKIE_SECURE = True`
- `SESSION_COOKIE_SECURE = True`
- `SECURE_HSTS_SECONDS = 31536000`
- `ALLOWED_HOSTS` spesifik (bukan wildcard)
- WhiteNoise untuk static files

⚠️ Perhatian:
- Jangan commit `.env` file ke GitHub
- Ganti SECRET_KEY dengan random value
- Gunakan HTTPS (PythonAnywhere support automatic)
- Backup database secara regular

---

## 📊 Monitoring

```bash
# Via PythonAnywhere Web tab:
- CPU usage
- Memory usage
- Error log (real-time)
- Server response time

# Via Bash Console:
cd /home/USERNAME/ammarpsbi

# Check database
python manage.py dbshell

# Clear cache
python manage.py clear_cache

# Create superuser if needed
python manage.py createsuperuser
```

---

## ❓ FAQ

**Q: Bagaimana create admin/superuser di production?**
```bash
python manage.py createsuperuser
# Then access at: https://USERNAME.pythonanywhere.com/admin
```

**Q: Bagaimana backup database?**
```bash
# Download db.sqlite3 dari Files tab
# Atau copy via Bash:
cp db.sqlite3 db.sqlite3.backup
```

**Q: Bagaimana restart app?**
```bash
# Di Web tab: Klik Reload button
# Atau set scheduled task untuk restart otomatis
```

**Q: Apakah ada uptime monitoring?**
```
Ya, PythonAnywhere menyediakan di Account tab → Services
```

---

## 📞 Support & Resources

- **PythonAnywhere Help:** https://www.pythonanywhere.com/help/
- **Django Docs:** https://docs.djangoproject.com/
- **WhiteNoise Docs:** http://whitenoise.evans.io/
- **Verify Script:** `python verify_pythonanywhere.py`

---

**Last Updated:** May 13, 2026
**Status:** Production Ready ✅
