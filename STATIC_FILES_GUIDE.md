# 🎨 Static Files Configuration untuk PythonAnywhere

Panduan mengatasi masalah tampilan (CSS, JavaScript) yang tidak muncul di PythonAnywhere.

---

## 🔍 Diagnosa Masalah

### Jika CSS/JavaScript tidak muncul:
- ❌ Halaman HTML loading tapi tidak ada styling (warna, layout jelek)
- ❌ JavaScript tidak berfungsi (hover effects, animations tidak jalan)
- ❌ Font Google tidak ter-load

---

## ✅ Solusi

### **Step 1: Pastikan STATIC_ROOT Benar**

Di **PythonAnywhere Web Tab**, pastikan:

```
Static files:
  URL: /static/
  Directory: /home/USERNAME/ammarpsbi/staticfiles
```

JANGAN menggunakan path lain seperti `static/` atau `/staticfiles/`

---

### **Step 2: Collect Static Files (PENTING!)**

**Di Bash Console PythonAnywhere, jalankan:**

```bash
cd /home/USERNAME/ammarpsbi
python manage.py collectstatic --noinput --clear
```

**Penjelasan:**
- `--noinput`: tidak ada prompt (automated)
- `--clear`: hapus static files lama terlebih dahulu (penting!)

**Output yang benar:**
```
Found 15 static files to collect
Collecting...
Copying '.../dashboard/static/dashboard/style.css'
Copying '.../dashboard/static/dashboard/auth.css'
Copying '.../dashboard/static/dashboard/script.js'
...
15 static files collected successfully.
```

---

### **Step 3: Verify Static Files**

**Di PythonAnywhere Files tab:**
1. Buka folder `/home/USERNAME/ammarpsbi/`
2. Cari folder `staticfiles/`
3. Dalam folder tersebut seharusnya ada:
   ```
   staticfiles/
   ├── dashboard/
   │   ├── style.css
   │   ├── auth.css
   │   └── script.js
   └── admin/
       ├── css/
       ├── js/
       └── ...
   ```

Jika folder `staticfiles/` tidak ada atau kosong, berarti `collectstatic` gagal.

---

### **Step 4: Reload Web App**

Setelah `collectstatic` selesai:
1. Tab **Web**
2. Klik tombol **Reload** (hijau)
3. Akses website Anda
4. CSS/JS seharusnya sudah muncul ✅

---

## 🛠️ Troubleshooting

### **Error: "No such file or directory"**

```bash
# Cek apakah path benar
ls /home/USERNAME/ammarpsbi/dashboard/static/
```

Output harus menunjukkan: `auth.css  script.js  style.css`

Jika tidak ada, berarti folder structure tidak benar di git clone.

---

### **Error: "You have not set STATIC_ROOT"**

Di `settings.py`, pastikan:
```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

Bukan:
```python
STATIC_ROOT = 'staticfiles'  # ❌ SALAH
STATIC_ROOT = '/staticfiles'  # ❌ SALAH
```

---

### **CSS Muncul Tapi Animation/JavaScript Tidak Jalan**

Kemungkinan masalah:
1. **JavaScript path salah di HTML**
   - Gunakan `{% static 'dashboard/script.js' %}`
   - Bukan path hardcoded seperti `<script src="/static/dashboard/script.js">`

2. **Template tidak load static tag**
   - Pastikan di atas HTML ada: `{% load static %}`

3. **Browser cache**
   - Hard refresh: `Ctrl+Shift+R` (Windows) atau `Cmd+Shift+R` (Mac)

---

### **STATICFILES_STORAGE Error**

Jika ada error tentang `whitenoise.storage.CompressedManifestStaticFilesStorage`:

```python
# Di settings.py, pastikan ada fallback
if DEBUG:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---

## 📋 Konfigurasi yang Sudah Diupdate

✅ **settings.py:**
- `STATIC_URL = '/static/'`
- `STATIC_ROOT = BASE_DIR / 'staticfiles'`
- `STATICFILES_DIRS = [BASE_DIR / 'dashboard' / 'static']`
- Conditional storage untuk development/production

✅ **urls.py:**
- Serve static files di development mode

✅ **MIDDLEWARE:**
- `'whitenoise.middleware.WhiteNoiseMiddleware'` untuk serve static files di production

---

## 🔄 Setelah Update di Local

Jika Anda update CSS/JS di local:

```bash
# 1. Test lokal
python manage.py collectstatic --noinput

# 2. Git push
git add .
git commit -m "Update static files"
git push origin main

# 3. Di PythonAnywhere
cd /home/USERNAME/ammarpsbi
git pull origin main
python manage.py collectstatic --noinput --clear

# 4. Reload web app
```

---

## 📚 File Referensi

- **settings.py** - Static files configuration
- **urls.py** - URL routing + static serving
- **dashboard/static/** - Lokasi CSS/JS files

---

## 💡 Tips

**Untuk debug, Anda bisa check status:** 
```bash
python manage.py findstatic dashboard/style.css --verbosity=2
```

**Atau check semua static files:**
```bash
python manage.py findstatic
```

---

**Last Updated:** May 13, 2026
**Status:** Static Files Properly Configured ✅
