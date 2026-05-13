# 🚀 Panduan Deployment ke PythonAnywhere (UPDATED)

Panduan lengkap untuk mendeploy project `ammarpsbi` ke PythonAnywhere dengan konfigurasi production-ready.

---

## ✅ File-File yang Sudah Dipersiapkan

- ✅ **settings.py** - Sudah dikonfigurasi untuk production mode (DEBUG=False)
- ✅ **requirements.txt** - Sudah include python-dotenv, whitenoise, Pillow
- ✅ **.env** - File environment variables (HARUS diisi username PythonAnywhere Anda)
- ✅ **pythonanywhere_wsgi.py** - WSGI file khusus untuk PythonAnywhere
- ✅ **.gitignore** - Sudah dikonfigurasi untuk mengabaikan file sensitif

---

## 📋 Langkah-Langkah Deployment

### **Langkah 1: Siapkan Repository Git**
```bash
# Jika belum ada git repo, buat satu
git init
git add .
git commit -m "Prepare for PythonAnywhere deployment"
```

### **Langkah 2: Upload ke GitHub**
1. Buat repository baru di GitHub (https://github.com/new)
2. Upload code Anda:
   ```bash
   git remote add origin https://github.com/USERNAME/ammarpsbi.git
   git branch -M main
   git push -u origin main
   ```

### **Langkah 3: Update .env File dengan Credentials PythonAnywhere**

**PENTING:** Sebelum deploy, edit file `.env`:
```bash
# Ubah nilai ini dengan username PythonAnywhere Anda
# Contoh: jika username PythonAnywhere Anda "ammar", maka:
ALLOWED_HOSTS=localhost,127.0.0.1,ammar.pythonanywhere.com
```

---

## 🔧 Setup di PythonAnywhere

### **Langkah 4: Bash Console - Clone Repository**

1. Login ke PythonAnywhere (https://www.pythonanywhere.com)
2. Buka **Bash Console** (di menu "Consoles")
3. Jalankan perintah berikut:
   ```bash
   # Clone repository Anda
   git clone https://github.com/USERNAME/ammarpsbi.git
   cd ammarpsbi
   
   # Buat virtual environment
   mkvirtualenv --python=/usr/bin/python3.10 venv
   
   # Install dependencies
   pip install -r requirements.txt
   ```

### **Langkah 5: Setup Database & Static Files**

Masih di Bash Console, jalankan:
```bash
# Migrasi database
python manage.py migrate

# Kumpulkan static files
python manage.py collectstatic --noinput
```

### **Langkah 6: Konfigurasi Tab "Web" di PythonAnywhere**

1. Go to **Web** tab di dashboard PythonAnywhere
2. Klik **"Add a new web app"**
3. Pilih **"Manual Configuration"** dan pilih Python 3.10

**Isi field berikut:**

**Virtualenv Section:**
- Virtualenv path: `/home/USERNAME/.virtualenvs/venv` 
  (atau cukup ketik `venv` jika PythonAnywhere bisa auto-detect)

**Code Section:**
- Source code: `/home/USERNAME/ammarpsbi`
- Working directory: `/home/USERNAME/ammarpsbi`

**Static Files Section:**
- URL: `/static/`
- Path: `/home/USERNAME/ammarpsbi/staticfiles`

### **Langkah 7: Setup WSGI Configuration**

1. Di tab **Web**, scroll ke bawah
2. Klik link **"WSGI configuration file"** (biasanya ada di section "Code")
3. Hapus semua isi file yang ada
4. Ganti dengan isi file **pythonanywhere_wsgi.py** dari project Anda:

```python
import os
import sys
from pathlib import Path

# Tambahkan path proyek ke sys.path
project_path = '/home/USERNAME/ammarpsbi'
if project_path not in sys.path:
    sys.path.insert(0, project_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project.settings')

from pathlib import Path
import dotenv

env_file = Path(project_path) / '.env'
dotenv.load_dotenv(env_file)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**⚠️ PENTING:** Ganti `USERNAME` dengan username PythonAnywhere Anda

### **Langkah 8: Reload Web App**

1. Scroll ke atas di tab **Web**
2. Klik tombol **Reload** (warna hijau)
3. Tunggu sampai status berubah menjadi "Running"

---

## 🔍 Testing & Troubleshooting

### **Cek apakah web app berjalan:**
- Akses: `https://USERNAME.pythonanywhere.com`
- Anda seharusnya melihat halaman login atau dashboard

### **Jika ada error:**

1. **Cek Error Log:**
   - Di tab Web, scroll ke bawah
   - Lihat **"Error log"** untuk detail error
   - Error log ini sangat membantu debugging

2. **Common Errors & Solutions:**

| Error | Solusi |
|-------|--------|
| **ModuleNotFoundError: No module named 'dotenv'** | Jalankan `pip install python-dotenv` di Bash Console |
| **No such file or directory: '.env'** | Pastikan .env file sudah di-upload ke PythonAnywhere |
| **Secret key error** | Periksa .env file, pastikan SECRET_KEY diisi |
| **Static files tidak muncul** | Jalankan `python manage.py collectstatic --noinput` |
| **Database error** | Jalankan `python manage.py migrate` lagi |

### **Cek Bash Console untuk debugging:**
```bash
# SSH ke PythonAnywhere
cd /home/USERNAME/ammarpsbi

# Test Django project
python manage.py shell
>>> from django.conf import settings
>>> print(settings.DEBUG)
>>> print(settings.ALLOWED_HOSTS)
```

---

## 🔐 Security Notes untuk Production

✅ **Sudah dikonfigurasi di settings.py:**
- `DEBUG = False` (environment-based)
- `CSRF_COOKIE_SECURE = True`
- `SESSION_COOKIE_SECURE = True`
- `SECURE_HSTS_SECONDS` enabled

⚠️ **Hal yang perlu diperhatian:**
1. Jangan commit `.env` file ke git (sudah di .gitignore)
2. Ganti SECRET_KEY di .env dengan nilai yang random untuk production
3. Gunakan HTTPS (PythonAnywhere support https automatic)

---

## 📊 Monitoring

Setelah deployment, Anda bisa monitoring di PythonAnywhere:
- **CPU usage** → Tab "Web"
- **Error logs** → Tab "Web", scroll ke bawah
- **Server logs** → Tab "Logs"

---

## 🔄 Update Code di Production

Setiap kali Anda update code:

1. **Push ke GitHub:**
   ```bash
   git add .
   git commit -m "Update message"
   git push origin main
   ```

2. **Pull di PythonAnywhere (Bash Console):**
   ```bash
   cd /home/USERNAME/ammarpsbi
   git pull origin main
   ```

3. **Reload web app** (Tab Web → Reload button)

**Tips:** Jika ada perubahan di database models, jalankan:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

---

## ❓ FAQ

**Q: Berapa lama setup ini?**
A: ~15-20 menit untuk pertama kali

**Q: Apakah database sqlite3 bisa di production?**
A: Bisa untuk small project, tapi for scaling better gunakan PostgreSQL

**Q: Bagaimana cara bikin superuser?**
A: Di Bash Console, jalankan:
```bash
python manage.py createsuperuser
```

**Q: URL admin apakah?**
A: `https://USERNAME.pythonanywhere.com/admin`

---

## 📞 Support

Jika ada pertanyaan, cek:
1. PythonAnywhere docs: https://www.pythonanywhere.com/help/
2. Django docs: https://docs.djangoproject.com/
3. Error log di PythonAnywhere tab Web
