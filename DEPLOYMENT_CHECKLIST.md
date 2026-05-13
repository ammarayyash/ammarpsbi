# ✅ Pre-Deployment Checklist untuk PythonAnywhere

Gunakan checklist ini untuk memastikan semua sudah siap sebelum deploy.

## 📝 File Configuration Checklist

- [ ] **settings.py** 
  - [ ] Import dotenv: `from dotenv import load_dotenv`
  - [ ] DEBUG settings menggunakan environment variable
  - [ ] ALLOWED_HOSTS menggunakan environment variable
  - [ ] WhiteNoise middleware sudah ditambahkan
  - [ ] STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

- [ ] **requirements.txt**
  - [ ] Django==5.1.3 ✓
  - [ ] djangorestframework==3.15.2 ✓
  - [ ] python-dotenv==1.0.1 ✓
  - [ ] whitenoise==6.6.0 ✓
  - [ ] Pillow==10.1.0 ✓

- [ ] **.env file**
  - [ ] Sudah dibuat
  - [ ] DEBUG=False
  - [ ] SECRET_KEY diisi (bukan insecure key)
  - [ ] ALLOWED_HOSTS berisi domain PythonAnywhere Anda
  - [ ] File TIDAK di-commit ke git (.gitignore sudah diupdate)

- [ ] **lms_project/wsgi.py**
  - [ ] Sudah import dotenv
  - [ ] Sudah load .env file

- [ ] **pythonanywhere_wsgi.py**
  - [ ] Sudah dibuat
  - [ ] USERNAME sudah diganti dengan username PythonAnywhere Anda

- [ ] **.gitignore**
  - [ ] `.env` sudah di-list
  - [ ] `db.sqlite3` sudah di-list
  - [ ] `staticfiles/` sudah di-list

## 🔐 Security Checklist

- [ ] DEBUG = False di environment
- [ ] SECRET_KEY menggunakan random string (bukan default)
- [ ] .env file tidak di-commit ke git
- [ ] CSRF_COOKIE_SECURE = True
- [ ] SESSION_COOKIE_SECURE = True
- [ ] ALLOWED_HOSTS menggunakan domain spesifik (bukan ['*'])

## 📦 Pre-Deployment Steps

- [ ] **Local Testing**
  ```bash
  python manage.py migrate
  python manage.py collectstatic --noinput
  python manage.py runserver
  ```

- [ ] **Git Repository**
  ```bash
  git init (jika belum ada)
  git add .
  git commit -m "Prepare for PythonAnywhere deployment"
  git remote add origin https://github.com/YOUR_USERNAME/ammarpsbi.git
  git push -u origin main
  ```

- [ ] **Update .env File**
  - [ ] ALLOWED_HOSTS sudah sesuai dengan domain PythonAnywhere
  - [ ] SECRET_KEY sudah diganti dengan random value
  - [ ] DEBUG = False

## 🚀 PythonAnywhere Setup Checklist

### Bash Console
- [ ] Clone repository: `git clone https://github.com/USERNAME/ammarpsbi.git`
- [ ] Masuk folder: `cd ammarpsbi`
- [ ] Buat virtualenv: `mkvirtualenv --python=/usr/bin/python3.10 venv`
- [ ] Install packages: `pip install -r requirements.txt`
- [ ] Migrate database: `python manage.py migrate`
- [ ] Collect static: `python manage.py collectstatic --noinput`

### Web Tab Configuration
- [ ] Add new web app → Manual Configuration
- [ ] Choose Python 3.10
- [ ] Virtualenv path: `/home/USERNAME/.virtualenvs/venv`
- [ ] Source code: `/home/USERNAME/ammarpsbi`
- [ ] Working directory: `/home/USERNAME/ammarpsbi`
- [ ] Static files: 
  - [ ] URL: `/static/`
  - [ ] Path: `/home/USERNAME/ammarpsbi/staticfiles`
- [ ] WSGI configuration file sudah diupdate

### WSGI File Configuration
- [ ] Hapus isi WSGI config file default
- [ ] Copy isi dari pythonanywhere_wsgi.py
- [ ] Ganti USERNAME dengan username PythonAnywhere Anda
- [ ] Save

### Final Steps
- [ ] Klik Reload button (hijau)
- [ ] Tunggu sampai "Running" status
- [ ] Akses https://USERNAME.pythonanywhere.com
- [ ] Verifikasi tidak ada error

## 🧪 Post-Deployment Testing

- [ ] Website bisa diakses
- [ ] Login page muncul
- [ ] Static files (CSS, JS) muncul dengan benar
- [ ] Media files bisa diakses
- [ ] Admin panel (/admin) bisa diakses
- [ ] Database queries berjalan normal

## 📊 Monitoring Post-Deployment

- [ ] Check error logs di PythonAnywhere Web tab setiap hari pertama
- [ ] Monitor CPU usage
- [ ] Test semua fitur utama aplikasi
- [ ] Set up automated backups untuk database

## 🔗 Useful Links

- PythonAnywhere Help: https://www.pythonanywhere.com/help/
- Django Deployment: https://docs.djangoproject.com/en/6.0/howto/deployment/
- WhiteNoise Docs: http://whitenoise.evans.io/en/stable/
- Deployment Guide: Lihat DEPLOYMENT_GUIDE.md

---

**Status:** Ready to Deploy ✅

Jika sudah semua checklist ini selesai, aplikasi Anda siap di-deploy ke PythonAnywhere!
