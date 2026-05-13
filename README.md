# Projek-PSBI

Panduan singkat: cara mengupload (push) proyek Django ini ke GitHub dan menjalankan CI dasar.

Langkah lokal (di direktori proyek):

1. Inisialisasi git dan commit:

```bash
git init
git add .
git commit -m "Initial commit"
```

2. Buat repository baru di GitHub (via web atau `gh` CLI). Contoh menggunakan `gh`:

```bash
gh repo create <username>/<repo-name> --public --source=. --remote=origin --push
```

3. Jika tidak menggunakan `gh`, buat repo di GitHub web dan jalankan:

```bash
git remote add origin https://github.com/<username>/<repo-name>.git
git branch -M main
git push -u origin main
```

Catatan deployment:
- GitHub Pages tidak cocok untuk aplikasi Django dinamis.
- Untuk menjalankan Django online, gunakan platform PaaS seperti Heroku, Railway, Render, atau digitalocean App Platform.

CI (GitHub Actions):
- Workflow dasar disertakan pada `.github/workflows/ci.yml` untuk menjalankan `python manage.py test` pada setiap push/PR.

Menjalankan secara lokal:

```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Jika mau, saya bisa juga:
- Menambahkan file `Procfile` untuk Heroku
- Menambahkan contoh konfigurasi `.env` dan instruksi deploy ke Railway/Render
