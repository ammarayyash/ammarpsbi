Berikut adalah dokumen spesifikasi gamifikasi web lengkap untuk 5 level yang telah kita buat. Ini murni teks penjelasan mekanisme, aturan main, input pengguna, logika skor otomatis, dan alur penyajian di browser — tanpa kode pemrograman, namun cukup rinci untuk diimplementasikan.
________________________________________
🎮 Spesifikasi Gamifikasi Web: Vector Master Challenge (Level 1–5)
1. Arsitektur Umum
•	Platform: Web browser (desktop/laptop direkomendasikan karena menggunakan Pen Tool simulasi).
•	Teknologi yang diasumsikan: HTML5, CSS, JavaScript, Canvas API, Fabric.js atau SVG.js, LocalStorage untuk menyimpan skor.
•	Struktur halaman:
o	Halaman utama → pilih level (terkunci sampai level sebelumnya selesai dengan skor minimal 60).
o	Setiap level memiliki halaman misi sendiri.
o	Setelah submit, tampilkan skor, umpan balik, dan tombol ke level berikutnya.
o	Papan peringkat (Leaderboard) disimpan di LocalStorage.
•	Sistem Skor Khusus:
Setiap level memiliki skor maksimal 100 + bonus.
Peserta harus mencapai minimal 60 poin untuk membuka level selanjutnya.
•	Penyimpanan data:
o	localStorage menyimpan: skor per level, status unlock, jawaban peserta (opsional).
o	Tidak perlu server backend.
________________________________________
2. Detil Misi per Level (Mekanisme Web)
🔹 Level 1 – The Discovery Quest
Tampilan Halaman:
•	10 gambar aset visual (ikon, foto, logo, tekstur, dll.) ditampilkan dalam grid 2×5.
•	Di bawah setiap gambar: dua tombol radio Vektor / Bitmap, dan kolom teks kecil (textarea) untuk alasan.
Cara Peserta Bermain:
•	Pilih jenis aset dan tulis alasan (min 10 karakter).
•	Klik tombol "Kumpulkan Jawaban".
Logika Skor Otomatis (JavaScript di belakang):
•	Setiap jawaban benar = +2 poin (total maks dari jawaban = 20).
•	Setiap alasan yang mengandung kata kunci (daftar: scalable, node, path, pecah, piksel, ukuran file, zoom, resolusi) = +1 poin per aset (maks 10 poin).
•	Bonus: Sistem membandingkan pilihan peserta terhadap "jawaban ekstrem" yang telah ditentukan (misal: aset #4 adalah logo perusahaan yang akan dicetak besar → jawaban benar adalah vektor). Jika peserta memilih kebalikannya (bitmap) untuk aset ekstrem, dan dalam alasan menyebut efek negatifnya, tetap bonus +5 poin karena sadar akan konsekuensi.
Deteksi bonus: Cek checkbox tersembunyi + kata kunci "cetak besar", "pecah", "buram".
•	Skor akhir = poin jawaban + poin alasan + bonus.
Maksimal = 20 (jawaban) + 10 (alasan) + 5 (bonus) = 35? Tidak, karena skor maks level 1 dikonversi ke 100. Maka:
o	Konversi: (skor_mentah / 35) * 100 dibulatkan.
•	Contoh: Peserta benar semua (20), alasan 8 kata kunci (8), bonus 5 → total 33/35 = 94,3 → skor tampil 94.
Umpan Balik:
•	Tampilkan jawaban benar/salah untuk setiap aset.
•	Tampilkan saran jika skor rendah: "Coba pelajari lagi perbedaan vektor & bitmap."
________________________________________
🔹 Level 2 – The Tracing Challenge
Tampilan Halaman:
•	Area kanvas (800×600 px) dengan gambar referensi logo (misal: Nike Swosh) sebagai background semi-transparan.
•	Toolbar: Pen Tool (bisa klik + drag untuk kurva), Direct Selection Tool (edit node), Hapus node, Reset.
•	Tombol: "Hitung Skor" (sebelum submit, peserta bisa lihat efisiensi sementara) dan "Submit Final".
Aturan Main:
•	Peserta harus menjiplak logo dengan jumlah anchor point sesedikit mungkin.
•	Setelah selesai, klik Submit.
Logika Skor Otomatis:
1.	Hitung jumlah anchor point yang dibuat peserta = X.
2.	Jumlah anchor referensi (sudah ditentukan dalam sistem) = R (misal: Nike = 12).
3.	Skor efisiensi = (R / X) * 100 (dibatasi maks 200, karena jika lebih sedikit dari referensi tetap bagus).
o	Jika X < R, skor efisiensi = 100 + (R - X) * 2 (maks 120).
4.	Penalti bentuk melenceng:
o	Sistem melakukan overlay perbandingan antara hasil tracing peserta dengan bentuk referensi.
o	Hitung rasio area berbeda dengan cara: render kedua bentuk ke canvas, hitung pixel yang tidak cocok. Jika rasio > 2%, kurangi 20 poin.
5.	Bonus kurva: Jika semua node yang dibuat peserta bertipe curve (bukan sudut tajam tanpa handle) dan logo bersifat organik, tambah +10 poin.
6.	Skor akhir = (efisiensi - penalti + bonus) dinormalisasi ke 100, dengan batas 0–100.
o	Contoh: X=8, R=12 → efisiensi = (12/8)*100 = 150 → dipotong jadi 120. Penalti 0, bonus 10 → skor mentah 130. Dikonversi ke 100 (karena maks 100 ditetapkan): min(130, 100) = 100.
Umpan Balik: "Efisiensi node bagus! Namun bentuk sedikit melenceng di bagian ekor."
________________________________________
🔹 Level 3 – The Mood Master
Tampilan Halaman:
•	Satu ilustrasi vektor statis (format SVG embedded) – misal: pemandangan gunung, rumah, matahari, pohon.
•	Tiga tab: Pagi, Siang, Malam.
•	Alat kontrol di setiap tab:
o	Color picker untuk setiap elemen (gunung, rumah, langit, matahari/bulan).
o	Dropdown Blending Mode (Normal, Multiply, Screen, Overlay) untuk layer bayangan.
o	Slider Gaussian Blur (0–10px) untuk efek glow atau kabut.
•	Tombol "Simpan Suasana" per tab, lalu "Kirim Ketiga Suasana".
Logika Skor Otomatis:
Sistem menilai setelah semua suasana dikirim.
•	Akurasi suasana (40 poin):
Analisis warna dominan setiap suasana menggunakan Canvas API → hitung rata-rata Hue.
o	Pagi: Hue antara 30–60 (kuning/oranye pastel).
o	Siang: Hue antara 50–80 (biru langit cerah).
o	Malam: Hue antara 200–280 (biru gelap/ungu).
Setiap suasana yang tepat mendapat 13,3 poin.
•	Kreativitas palet (30 poin):
o	Hitung jumlah warna unik yang digunakan di ketiga suasana (minimal 6 warna berbeda).
o	Tingkat kontras antar elemen (deteksi perbedaan luminance).
Poin = (jumlah warna unik / 10) * 15 + (skor kontras / 10) * 15.
•	Penggunaan blending mode & blur (20 poin):
o	Terdeteksi jika setidaknya 1 elemen menggunakan blending mode bukan Normal (+10).
o	Terdeteksi jika ada slider blur > 0 di salah satu suasana (+10).
•	Kebersihan (10 poin):
o	Apakah peserta menggunakan fitur "Global Color" (jika ada dalam editor web)? Tidak wajib, tapi jika ada, +5.
o	Apakah layer dinamai dengan jelas (default jika sistem menyediakan, otomatis dapat 5).
Skor akhir = penjumlahan langsung (maks 100).
Umpan balik contoh: "Malam-mu berhasil! Tapi siang sedikit terlalu gelap."
________________________________________
🔹 Level 4 – Mascot Creator
Tampilan Halaman:
•	Menampilkan creative brief (diambil secara acak dari array 4–5 brief berbeda).
•	Area editor vektor web sederhana (Fabric.js) dengan tools: Pen, Brush, Shape, Rectangle, Ellipse, Text, Symbol Sprayer (lingkaran, bintang, daun).
•	Layer panel (tambah, hapus, ganti nama).
•	Tombol unggah sketsa (file image) + tombol "Simpan Final" (menyimpan SVG).
Logika Skor Otomatis (100 poin):
•	Kesesuaian brief (30 poin):
Sistem membandingkan teks deskripsi singkat yang ditulis peserta (wajib diisi 50 kata) dengan kata kunci dari brief.
Contoh brief: "ramah, daun, remaja" → jika deskripsi mengandung minimal 2 dari 3 kata kunci, dapat 30.
•	Kebersihan inking (20 poin):
Ekstrak semua path dari SVG, hitung total node. Jika node < 200 → 20, 200–400 → 10, >400 → 5.
•	Layering strategy (20 poin):
Minimal ada 4 layer dengan nama tidak default (Layer 1, Layer 2 tidak dihitung). Setiap layer bernama jelas (head, body, background) mendapat poin.
•	Penggunaan tekstur & symbol sprayer (20 poin):
o	Ada elemen simbol sprayer (misal: bintang, daun berulang) → +10.
o	Ada efek tekstur (grain/noise) yang diterapkan (deteksi filter SVG) → +10.
•	Orisinalitas (10 poin):
Sistem membandingkan silhouette maskot dengan database silhouette populer (misal: Pikachu, Mickey) menggunakan perbedaan pixel sederhana. Jika kemiripan < 70% → 10 poin.
Flow: Peserta simpan sketsa + final, klik "Kirim". Skor muncul.
________________________________________
🔹 Level 5 – The Client Handover
Tampilan Halaman: Wizard 4 langkah.
Langkah 1 – Cleaning Paths
•	Sistem menampilkan SVG "kotor" (banyak node, teks belum outline).
•	Tool: simplify path slider, tombol outline text, tombol gabung path.
•	Setelah selesai, klik "Next".
Langkah 2 – Export Settings
•	Menampilkan tabel 3 baris: (1) Stiker kopi 3×3 cm, (2) Web dashboard, (3) Billboard 2×3 m.
•	Peserta memilih format dari dropdown (PDF, EPS, SVG, PNG, JPG), ukuran, dan mode warna (RGB/CMYK).
•	Klik "Next".
Langkah 3 – Mockup Presentation
•	Sistem memberikan 3 template mockup (stiker, web mockup, billboard).
•	Peserta drag-and-drop hasil desainnya ke area mockup, lalu atur posisi/ukuran.
•	Klik "Next".
Langkah 4 – Asset Packaging & Brand Manual
•	Virtual folder tree: /Source, /Export, /Mockup, /Manual.pdf.
•	Peserta bisa memindahkan file (drag) ke folder yang sesuai.
•	Isi teks brand manual (nama brand, palet warna CMYK/RGB, aturan ruang kosong).
•	Klik "Submit Final".
Logika Skor Otomatis:
Kriteria	Bobot	Deteksi
Cleaning paths	30	Jumlah node pada path final ≤ 80% node awal, dan semua teks sudah menjadi path.
Export tepat	25	Cocokkan pilihan format dengan solusi ideal (stiker: PNG/PDF; web: SVG; billboard: EPS/PDF dengan CMYK). Setiap baris benar = 8,3 poin.
Mockup rapi	20	Deteksi apakah desain berada di dalam area mockup tanpa terpotong (bounding box check). nilai 0–20.
Struktur folder + manual	25	Folder berisi minimal 3 dari 4 folder, dan manual teks mengandung kata "palet", "CMYK", "RGB", "ruang kosong".
Bonus +10 jika peserta menyertakan file source (.ai atau .svg source) di folder /Source.
Skor akhir = total + bonus, dibatasi 100.
________________________________________
3. Alur Pengguna di Web
1.	Buka halaman utama → lihat 5 level dalam bentuk kartu (terkunci kecuali level 1).
2.	Klik Level 1 → kerjakan misi → dapat skor. Jika ≥60, level 2 terbuka.
3.	Ulangi hingga level 5.
4.	Setelah menyelesaikan semua level, tampilkan sertifikat kelulusan (text + download sebagai PNG) dan total skor keseluruhan (maks 500).
5.	Leaderboard menyimpan skor total setiap peserta (hanya di browser yang sama).
________________________________________
4. Catatan Implementasi Web (Tanpa Kode, Hanya Keterangan)
•	Canvas API cukup untuk deteksi bentuk (level 2), analisis warna (level 3), perbandingan silhouette (level 4).
•	Fabric.js atau Two.js bisa digunakan untuk editor vektor sederhana di level 4 dan 5.
•	LocalStorage menyimpan semua progres.
•	Tidak perlu backend – semua berjalan di sisi klien.
•	Tantangan teknis (yang "tidak masalah sulit diprogram") seperti deteksi kemiripan bentuk atau analisis histogram warna dapat diatasi dengan pustaka JavaScript yang sudah ada.
________________________________________
Dengan spesifikasi ini, programmer web dapat membangun sistem gamifikasi yang fungsional tanpa perlu menjelaskan ulang aturan main. Selamat membangun Vector Master Challenge! 🚀

