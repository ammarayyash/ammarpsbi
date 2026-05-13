# Kerangka Materi & Kebutuhan Modul (Vector Master Challenge)

Dokumen ini adalah acuan untuk membuat Modul PDF yang akan diunggah ke website. Setiap modul PDF sebaiknya mencakup poin-berikut agar selaras dengan sistem gamifikasi di web.

---

## 📂 Struktur Folder Modul (Saran)
Nanti silakan buat folder dengan struktur seperti ini:
- `media/modul/level1.pdf`
- `media/modul/level2.pdf`
- `...`

---

## 🛠️ Rincian Kebutuhan Konten per Level

### 📗 Level 1: Pengenalan Vektor & Bitmap
**Kebutuhan di PDF:**
- Gambar perbandingan resolusi (zoom-in piksel vs smooth vector).
- Daftar ekstensi file (SVG, AI, EPS vs JPG, PNG, GIF).
- Penjelasan skema penggunaan (kapan pakai vektor, kapan pakai foto).

### 📘 Level 2: Anatomi Path & Pen Tool
**Kebutuhan di PDF:**
- Diagram Anchor Point, Path, dan Handle.
- Tips "The Power of Less": Mengapa sedikit node lebih baik.
- Panduan menggunakan tombol shortcut (P untuk Pen, V untuk Select, A untuk Direct Select).

### 📙 Level 3: Teori Warna & Pencahayaan
**Kebutuhan di PDF:**
- Lingkaran warna (Color Wheel).
- Perbedaan profil warna RGB (Layar) vs CMYK (Cetak).
- Visualisasi Blending Modes (Multiply, Screen, Overlay).
- Contoh ilustrasi pagi, siang, dan malam dengan palet warna berbeda.

### 📒 Level 4: Karakter & Brief Kreatif
**Kebutuhan di PDF:**
- Cara membaca "Creative Brief" (mencari kata kunci).
- Tahapan menggambar: Sketsa -> Inking -> Coloring.
- Contoh hirarki layer yang rapi (Kepala, Mata, Mulut, Tubuh).

### 📕 Level 5: Finalisasi & Standar Industri
**Kebutuhan di PDF:**
- Checklist sebelum kirim: Cek node bocor, convert teks ke outline.
- Pengenalan format file untuk berbagai media (Cetak vs Web).
- Cara membuat folder "Final Handover" yang profesional untuk klien.

---

## 🔗 Rencana Integrasi ke Web
Setelah PDF Anda siap, saya akan membantu melakukan hal berikut:
1.  **Update Model**: Menambahkan field `pdf_file` pada model `Mission` (jika belum ada).
2.  **Update Template**: Memasang PDF Viewer (menggunakan `<iframe>` atau `embed`) pada halaman `materi.html`.
3.  **Populate Data**: Memasukkan link file PDF tersebut ke masing-masing misi di database.

---
*Silakan berikan folder modul jika sudah siap, saya akan langsung memproses integrasinya ke halaman materi.*
