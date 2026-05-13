# Lampiran

Berikut adalah daftar sumber daya, teknologi, dan aset yang digunakan dalam pengembangan proyek ini:

## 1. Daftar Teknologi (Tech Stack)
- **Framework:** Django 4.2+ (Python)
- **Frontend Library:** 
    - [Fabric.js](http://fabricjs.com/) (Vector Canvas Engine)
    - [FontAwesome](https://fontawesome.com/) (Icons)
    - [Google Fonts](https://fonts.google.com/) (Typography: Inter, Roboto)
- **Styling:** Custom Vanilla CSS with Glassmorphism UI patterns.

## 2. Daftar Aset Visual
- **Level 1 Assets:** Berbagai ikon format SVG dan gambar bitmap (JPEG/PNG) untuk tantangan identifikasi.
- **Level 2 References:** Logo referensi untuk tantangan pen-tool (Nike, Apple, Twitter).
- **Level 3 Illustrations:** SVG Illustration of Landscape (Day, Evening, Night sets).
- **Mascot Templates:** Silhouette database untuk deteksi orisinalitas pada Level 4.

## 3. Struktur Database Utama
- **UserProfile:** Menyimpan data XP, Level, Streak, dan Avatar.
- **Mission:** Detail level gamifikasi, hadiah XP, dan mode permainan.
- **UserMissionProgress:** Status progres pengguna di setiap level (not_started, reading, quiz, completed).
- **Question & Choice:** Data kuis evaluasi untuk setiap misi.

## 4. Tautan Referensi
- Dokumentasi Django: [https://docs.djangoproject.com/](https://docs.djangoproject.com/)
- Dokumentasi Fabric.js: [http://fabricjs.com/docs/](http://fabricjs.com/docs/)
- MDN Web Docs (Canvas API): [https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)

## 5. Panduan Instalasi Singkat
1. Clone repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Jalankan migrasi: `python manage.py migrate`.
4. Jalankan server: `python manage.py runserver`.
