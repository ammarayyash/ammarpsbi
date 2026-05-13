# Panduan Instalasi Lengkap ke PythonAnywhere

Panduan ini menjelaskan langkah-langkah untuk mendistribusikan proyek Django Anda ke PythonAnywhere, termasuk solusi untuk peringatan "No virtualenv detected".

## 1. Penjelasan Error: "Warning: No virtualenv detected"
Peringatan ini muncul karena Anda telah mengisi **Path Virtualenv** di tab "Web", tetapi folder virtualenv tersebut belum benar-benar dibuat di dalam file system PythonAnywhere.

**Cara Memperbaikinya:** Anda harus membuat virtualenv terlebih dahulu melalui **Bash Console** (lihat langkah 3 di bawah).

---

## 2. Langkah-langkah Instalasi Lengkap

### Langkah 1: Upload Code ke PythonAnywhere
Cara terbaik adalah menggunakan Git. Buka **Bash Console** di PythonAnywhere dan jalankan:
```bash
git clone https://github.com/username/repository-anda.git
cd repository-anda
```

### Langkah 2: Buat Virtual Environment
Di dalam folder proyek Anda di Bash Console, jalankan perintah ini:
```bash
# Ganti 'myenv' dengan nama yang Anda inginkan (misal: venv)
# Gunakan python versi yang sesuai (3.10 adalah pilihan aman di PA)
mkvirtualenv --python=/usr/bin/python3.10 venv
```
*Setelah ini, virtualenv akan otomatis aktif (ditandai dengan `(venv)` di depan prompt).*

### Langkah 3: Install Dependensi
Pastikan file `requirements.txt` sudah bersih (hanya Django dan DRF seperti yang kita buat tadi). Jalankan:
```bash
pip install -r requirements.txt
```

### Langkah 4: Konfigurasi Database & Static Files
Jalankan perintah Django standar:
```bash
python manage.py migrate
python manage.py collectstatic
```

### Langkah 5: Konfigurasi Tab "Web" di PythonAnywhere
Buka dashboard PythonAnywhere -> Tab **Web**.
1. **Add a new web app**: Pilih "Manual Configuration" (karena kita sudah punya kode). Pilih versi Python yang sama dengan saat membuat virtualenv (misal 3.10).
2. **Virtualenv Section**: Masukkan nama virtualenv Anda di kotak isian. Jika Anda menggunakan `mkvirtualenv venv`, cukup ketik `venv`. PythonAnywhere akan mendeteksi path lengkapnya secara otomatis.
   * *Setelah ini, peringatan "No virtualenv" seharusnya hilang.*
3. **Code Section**:
   * **Source code**: Isi dengan path ke folder root proyek Anda (misal: `/home/username/ammarpsbi`).
   * **Working directory**: Sama dengan Source code.
4. **Static Files Section**:
   * URL: `/static/`
   * Path: `/home/username/ammarpsbi/staticfiles` (sesuaikan dengan `STATIC_ROOT` di settings.py).

### Langkah 6: Edit File WSGI Configuration
Di tab Web, klik link **"WSGI configuration file"**. Hapus isinya dan ganti dengan ini:

```python
import os
import sys

# Tambahkan path proyek Anda ke sys.path
path = '/home/username/ammarpsbi'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'lms_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
*Ganti `username` dengan username PythonAnywhere Anda dan `ammarpsbi` dengan nama folder proyek Anda.*

### Langkah 7: Reload
Klik tombol **Reload** hijau di bagian atas tab Web. Selesai!

---

## 3. Tips Tambahan
* Jika ada error `Internal Server Error`, cek **Error Log** di bagian bawah tab Web.
* Untuk melihat perubahan kode, Anda harus selalu menekan tombol **Reload**.
