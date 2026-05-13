# Panduan Deployment Django ke PythonAnywhere

Berikut adalah langkah-langkah untuk mendeploy project LMS Django Anda ke [PythonAnywhere](https://www.pythonanywhere.com/).

## 1. Persiapan Akun & Upload File
1. Daftar atau login ke akun PythonAnywhere Anda.
2. Buka tab **Files** dan upload project Anda. Cara paling disarankan adalah dengan menggunakan GitHub (lalu di-clone di Bash PythonAnywhere), atau kompres folder project menjadi `.zip` lalu upload dan ekstrak di PythonAnywhere.
   - *Catatan:* Pastikan folder project yang Anda upload mengandung file `manage.py`.

## 2. Setup Virtual Environment
1. Buka tab **Consoles** dan mulai sebuah **Bash** console baru.
2. Buat virtual environment dengan versi Python yang sesuai (misal Python 3.10):
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 myvenv
   ```
3. Pindah ke direktori project Anda:
   ```bash
   cd ~/nama_folder_project_anda
   ```
   *(Ganti `nama_folder_project_anda` dengan folder yang berisi `manage.py`, misal: `projek-psbi`)*
4. Install semua requirements:
   ```bash
   pip install -r requirements.txt
   ```

## 3. Penyesuaian `settings.py`
Agar Django siap berjalan di production, lakukan beberapa penyesuaian di `lms_project/settings.py`. Anda dapat mengeditnya langsung dari tab **Files** di PythonAnywhere.

- Ubah `ALLOWED_HOSTS` untuk mengizinkan domain PythonAnywhere Anda:
  ```python
  ALLOWED_HOSTS = ['username_anda.pythonanywhere.com']
  ```
  *(Ganti `username_anda` dengan username PythonAnywhere Anda)*
- Set `DEBUG` menjadi `False` untuk keamanan production (opsional jika Anda masih ingin melihat error secara detail saat testing):
  ```python
  DEBUG = False
  ```
- Tambahkan `STATIC_ROOT` di bagian bawah (di bawah `STATIC_URL`) agar file statis bisa dikumpulkan:
  ```python
  import os # pastikan import os ada di bagian atas jika menggunakan os.path
  # atau gunakan BASE_DIR
  STATIC_ROOT = BASE_DIR / 'staticfiles'
  ```

## 4. Migrasi & Collectstatic
Di Bash console yang sama, jalankan perintah berikut:
```bash
# Melakukan migrasi database
python manage.py migrate

# Mengumpulkan file statis (Pilih 'yes' jika ditanya)
python manage.py collectstatic
```

## 5. Setup Web App di PythonAnywhere
1. Buka tab **Web** lalu klik **Add a new web app**.
2. Klik Next, lalu pilih **Manual Configuration** (Penting! Jangan pilih Django, pilih Manual).
3. Pilih versi Python yang sama dengan yang Anda gunakan saat membuat virtual environment (misal Python 3.10).
4. Klik Next hingga selesai.

## 6. Konfigurasi Path & Virtualenv
Di halaman konfigurasi Web App Anda (masih di tab Web):
1. **Virtualenv:** Pada bagian Virtualenv, masukkan path virtualenv yang tadi dibuat:
   `/home/username_anda/.virtualenvs/myvenv`
2. **Code:** Pada bagian Code, pastikan **Source code** dan **Working directory** mengarah ke direktori project Anda (yang berisi `manage.py`):
   `/home/username_anda/nama_folder_project_anda`

## 7. Konfigurasi WSGI
Di bagian Code, klik link **WSGI configuration file** (biasanya bernama `username_anda_pythonanywhere_com_wsgi.py`). Hapus semua isinya, lalu ganti dengan kode berikut:

```python
import os
import sys

# Tambahkan path ke folder project Anda (folder yang berisi manage.py)
path = '/home/username_anda/nama_folder_project_anda'
if path not in sys.path:
    sys.path.append(path)

# Beritahu Django di mana letak settings.py
os.environ['DJANGO_SETTINGS_MODULE'] = 'lms_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
*Jangan lupa ganti `username_anda` dan `nama_folder_project_anda` sesuai milik Anda.*
Simpan (Save) file tersebut.

## 8. Konfigurasi Static Files & Media
Django tidak melayani file statis secara langsung saat production (`DEBUG=False`), kita harus mengatur PythonAnywhere untuk melayaninya:
Di tab **Web**, scroll ke bagian **Static files**:

1. **Untuk Static Files:**
   - **URL:** `/static/`
   - **Directory:** `/home/username_anda/nama_folder_project_anda/staticfiles/`
2. **Untuk Media Files (Uploads):**
   - **URL:** `/media/`
   - **Directory:** `/home/username_anda/nama_folder_project_anda/media/`

## 9. Reload dan Selesai!
Scroll ke bagian paling atas di tab **Web** dan klik tombol hijau besar **Reload username_anda.pythonanywhere.com**.
Sekarang Anda bisa membuka URL web Anda dan mengecek apakah aplikasi sudah berjalan dengan normal.
