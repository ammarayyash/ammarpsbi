import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project.settings')
django.setup()

from dashboard.models import Mission, Question, Choice, CommunityRoom

def run():
    Mission.objects.all().delete()

    # ===== MISI 1: Pengenalan Gambar Vektor vs Raster =====
    m1 = Mission.objects.create(
        title="The Vector Architect (Fondasi & Navigasi)",
        description="Bangun fondasi yang kokoh sebelum mendirikan menara.",
        xp_reward=100,
        content="""
        <h2>Materi Utama</h2>
        <h3>1. Anatomi Vektor vs Bitmap</h3>
        <p>Dalam dunia desain digital, terdapat dua jenis utama gambar: vektor dan bitmap.</p>
        <p>Vektor adalah gambar yang dibentuk dari perhitungan matematis berupa garis dan kurva. Elemen penyusunnya terdiri dari node dan path. Karena berbasis matematika, gambar vektor dapat diperbesar atau diperkecil tanpa kehilangan kualitas (tidak pecah). Selain itu, ukuran file vektor biasanya lebih kecil dan efisien.</p>
        <p>Sebaliknya, bitmap (atau raster) tersusun dari kumpulan piksel. Setiap piksel memiliki warna tertentu, sehingga ketika gambar diperbesar, piksel-piksel tersebut akan terlihat dan menyebabkan gambar menjadi pecah atau buram. Bitmap sangat cocok untuk foto atau gambar dengan detail kompleks dan gradasi warna yang halus.</p>

        <h3>2. Antarmuka Perangkat Lunak (Adobe Illustrator / Figma)</h3>
        <p>Untuk bekerja dengan desain vektor, kita menggunakan perangkat lunak seperti Adobe Illustrator atau Figma. Keduanya memiliki antarmuka yang mirip secara konsep.</p>
        <p>Beberapa bagian penting yang perlu dipahami:</p>
        <ul>
            <li>Toolbar: Berisi alat-alat utama untuk menggambar dan mengedit.</li>
            <li>Properties Panel: Menampilkan pengaturan dari objek yang dipilih.</li>
            <li>Layers: Mengatur susunan objek agar desain lebih terorganisir.</li>
            <li>Artboard: Area kerja tempat kita membuat desain.</li>
        </ul>
        <p>Shortcut esensial yang wajib diingat:</p>
        <ul>
            <li>V → Select Tool</li>
            <li>A → Direct Selection Tool</li>
            <li>Z → Zoom Tool</li>
            <li>Ctrl/Cmd + S → Menyimpan pekerjaan</li>
        </ul>
        <p>Penguasaan shortcut akan mempercepat alur kerja secara signifikan.</p>

        <h3>3. Pengaturan Artboard Standar Industri</h3>
        <p>Artboard adalah kanvas digital tempat kita bekerja. Ukuran artboard harus disesuaikan dengan kebutuhan proyek.</p>
        <p>Beberapa ukuran yang umum digunakan:</p>
        <ul>
            <li>1920 × 1080 px → Untuk desain web atau presentasi (Full HD)</li>
            <li>1080 × 1080 px → Untuk konten media sosial (Instagram feed)</li>
            <li>A4 (210 × 297 mm) → Untuk kebutuhan cetak</li>
        </ul>
        <p>Praktik penting: Selalu simpan pengaturan artboard sebagai template jika sering digunakan. Ini akan menghemat waktu dan menjaga konsistensi desain.</p>

        <h2>Konsep Kunci</h2>
        <table style="width:100%; border-collapse: collapse; margin: 16px 0;">
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                <th style="padding: 12px; text-align: left; color: #818cf8;">Istilah</th>
                <th style="padding: 12px; text-align: left; color: #818cf8;">Penjelasan</th>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 12px;">Nodes</td>
                <td style="padding: 12px;">Titik kontrol yang menghubungkan segmen garis.</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 12px;">Paths</td>
                <td style="padding: 12px;">Rangkaian node yang membentuk bentuk vektor.</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 12px;">Handles</td>
                <td style="padding: 12px;">Tuas pada node kurva untuk mengatur kelengkungan.</td>
            </tr>
            <tr>
                <td style="padding: 12px;">Scalability</td>
                <td style="padding: 12px;">Kemampuan diperbesar atau diperkecil tanpa kehilangan kualitas.</td>
            </tr>
        </table>

        <h2>Penutup</h2>
        <p>Level ini adalah dasar dari semua kemampuan desain vektor. Memahami perbedaan vektor dan bitmap, mengenal antarmuka, serta menguasai artboard akan menjadi bekal penting sebelum masuk ke tahap desain yang lebih kompleks. Ingat, fondasi yang kuat akan menentukan seberapa tinggi "menara" desain yang bisa kamu bangun.</p>
        """,
        order=1
    )

    q1 = Question.objects.create(mission=m1, text="Apa yang menjadi basis dari gambar vektor?", order=1)
    Choice.objects.create(question=q1, text="Piksel", is_correct=False)
    Choice.objects.create(question=q1, text="Rumus matematika (titik, garis, kurva)", is_correct=True)
    Choice.objects.create(question=q1, text="Kumpulan foto", is_correct=False)
    Choice.objects.create(question=q1, text="Layer bitmap", is_correct=False)

    q2 = Question.objects.create(mission=m1, text="Apa yang terjadi pada gambar vektor saat diperbesar?", order=2)
    Choice.objects.create(question=q2, text="Gambar menjadi pecah/blur", is_correct=False)
    Choice.objects.create(question=q2, text="Ukuran file membesar drastis", is_correct=False)
    Choice.objects.create(question=q2, text="Gambar tetap tajam tanpa kehilangan kualitas", is_correct=True)
    Choice.objects.create(question=q2, text="Warna gambar berubah", is_correct=False)

    # ===== MISI 2: Tools Desain Vektor =====
    m2 = Mission.objects.create(
        title="Path Tamer (Kendali Garis Presisi)",
        description="Hanya dengan beberapa node, kau bisa meliukkan garis sesukamu.",
        xp_reward=100,
        content="""
        <h2>Materi Utama</h2>
        <h3>1. Penguasaan Pen Tool Tingkat Lanjut</h3>
        <p>Pen Tool adalah alat paling kuat dalam desain vektor, tetapi juga paling menantang untuk dikuasai.</p>
        <ul>
            <li>Membuat kurva: Klik lalu drag untuk memunculkan handle dan mengatur arah lengkungan.</li>
            <li>Mengubah jenis node: Gunakan Convert Anchor Point Tool (Shift + C) untuk mengubah node tajam menjadi kurva atau sebaliknya.</li>
            <li>Menghapus node berlebih: Gunakan fitur Simplify Path atau hapus manual untuk menjaga path tetap bersih dan ringan.</li>
        </ul>
        <p>Semakin sedikit node, semakin rapi dan fleksibel desainmu.</p>

        <h3>2. Manipulasi Bezier Curves</h3>
        <p>Bezier curve adalah dasar dari semua kurva dalam desain vektor.</p>
        <p>Hal penting yang perlu dipahami:</p>
        <ul>
            <li>Panjang handle menentukan tingkat kelengkungan.</li>
            <li>Arah handle menentukan arah kurva.</li>
        </ul>
        <p>Tips praktis:</p>
        <ul>
            <li>Handle pendek → sudut lebih tajam.</li>
            <li>Handle panjang → kurva lebih halus dan landai.</li>
        </ul>
        <p>Kontrol Bezier yang baik akan membuat desain terlihat profesional dan presisi.</p>

        <h3>3. Boolean Operations (Pathfinder)</h3>
        <p>Boolean operations digunakan untuk menggabungkan atau memotong bentuk.</p>
        <p>Operasi utama:</p>
        <ul>
            <li>Unite → Menggabungkan beberapa objek menjadi satu.</li>
            <li>Minus Front → Mengurangi objek depan dari objek belakang.</li>
            <li>Intersect → Menyisakan area yang saling bertumpuk.</li>
            <li>Exclude → Menghapus area tumpang tindih, menyisakan bagian luar.</li>
        </ul>
        <p>Dengan teknik ini, kamu bisa membangun bentuk kompleks dari kombinasi bentuk sederhana seperti lingkaran dan persegi.</p>

        <h2>Konsep Kunci</h2>
        <table style="width:100%; border-collapse: collapse; margin: 16px 0;">
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                <th style="padding: 12px; text-align: left; color: #818cf8;">Istilah</th>
                <th style="padding: 12px; text-align: left; color: #818cf8;">Penjelasan</th>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 12px;">Join</td>
                <td style="padding: 12px;">Menggabungkan dua node terbuka menjadi satu path.</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 12px;">Average</td>
                <td style="padding: 12px;">Menyamakan posisi node secara vertikal/horizontal (Align).</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 12px;">Outline Stroke</td>
                <td style="padding: 12px;">Mengubah stroke menjadi objek terisi (berguna untuk boolean).</td>
            </tr>
            <tr>
                <td style="padding: 12px;">Corner Radius</td>
                <td style="padding: 12px;">Mengatur sudut menjadi tumpul atau tajam pada bentuk geometris.</td>
            </tr>
        </table>

        <h2>Penutup</h2>
        <p>Pada level ini, kamu mulai benar-benar "menjinakkan" garis. Kemampuan mengontrol node, handle, dan operasi bentuk akan membuka jalan untuk membuat ilustrasi yang lebih kompleks, presisi, dan profesional. Ingat: bukan banyaknya node yang membuat desain hebat, tapi bagaimana kamu mengendalikannya.</p>
        """,
        order=2
    )

    q3 = Question.objects.create(mission=m2, text="Manakah software desain vektor yang gratis dan open-source?", order=1)
    Choice.objects.create(question=q3, text="Adobe Illustrator", is_correct=False)
    Choice.objects.create(question=q3, text="CorelDRAW", is_correct=False)
    Choice.objects.create(question=q3, text="Inkscape", is_correct=True)
    Choice.objects.create(question=q3, text="Photoshop", is_correct=False)

    q4 = Question.objects.create(mission=m2, text="Software vektor apa yang paling populer di percetakan Indonesia?", order=2)
    Choice.objects.create(question=q4, text="Inkscape", is_correct=False)
    Choice.objects.create(question=q4, text="CorelDRAW", is_correct=True)
    Choice.objects.create(question=q4, text="GIMP", is_correct=False)
    Choice.objects.create(question=q4, text="Canva", is_correct=False)

    # ===== MISI 3: Bezier Curves, Paths & Shapes =====
    m3 = Mission.objects.create(
        title="Color Alchemist (Estetika & Dimensi)",
        description="Dari palet yang sama, kau ciptakan pagi, siang, dan malam.",
        xp_reward=100,
        content="""
        <h2>Materi Utama</h2>
        <h3>1. Teori Warna Digital (RGB untuk layar)</h3>
        <p>Dalam desain digital, warna bekerja dalam sistem RGB (Red, Green, Blue) yang digunakan untuk layar.</p>
        <ul>
            <li>RGB → Digunakan untuk layar digital (HP, monitor, web).</li>
            <li>CMYK → Digunakan untuk cetak (printer).</li>
        </ul>
        <p>Warna dalam RGB direpresentasikan dengan:</p>
        <ul>
            <li>Nilai 0–255 untuk masing-masing kanal (R, G, B).</li>
            <li>Kode Hex (misalnya: #FF5733) sebagai representasi singkat warna.</li>
        </ul>
        <p>Memahami keseimbangan warna penting agar desain tidak terlalu mencolok atau terlalu redup.</p>

        <h3>2. Teknik Lanjutan</h3>
        <p><strong>Gradient Mesh</strong></p>
        <p>Teknik ini memungkinkan pembuatan gradasi kompleks dengan banyak titik warna, sehingga menghasilkan efek realistis (misalnya bayangan wajah atau objek 3D halus).</p>
        <p><strong>Blending Modes</strong></p>
        <p>Mode pencampuran menentukan bagaimana satu layer berinteraksi dengan layer di bawahnya:</p>
        <ul>
            <li>Multiply → Membuat efek bayangan (lebih gelap).</li>
            <li>Screen → Membuat efek cahaya (lebih terang).</li>
            <li>Overlay → Kombinasi kontras terang dan gelap.</li>
        </ul>
        <p><strong>Shading & Lighting</strong></p>
        <p>Menentukan arah cahaya sangat penting dalam memberi dimensi:</p>
        <ul>
            <li>Soft shadow → Bayangan halus, natural.</li>
            <li>Hard shadow → Bayangan tajam, kontras tinggi.</li>
        </ul>
        <p>Konsistensi arah cahaya akan membuat desain terasa lebih realistis.</p>

        <h3>3. Alat Bantu</h3>
        <ul>
            <li>Opacity Mask → Mengatur transparansi menggunakan gradasi grayscale.</li>
            <li>Gaussian Blur → Efek blur lembut untuk bayangan atau cahaya.</li>
            <li>Global Colors → Warna yang terhubung ke banyak objek dan bisa diubah sekaligus.</li>
        </ul>
        <p>Tools ini membantu mempercepat workflow dan menjaga konsistensi visual.</p>

        <h2>Konsep Kunci</h2>
        <table style="width:100%; border-collapse: collapse; margin: 16px 0;">
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                <th style="padding: 12px; text-align: left; color: #818cf8;">Istilah</th>
                <th style="padding: 12px; text-align: left; color: #818cf8;">Penjelasan</th>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 12px;">Color Palettes</td>
                <td style="padding: 12px;">Kumpulan warna harmonis (monokromatik, analogus, komplementer).</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 12px;">Global Colors</td>
                <td style="padding: 12px;">Warna di Swatches yang jika diubah akan memengaruhi semua objek terkait.</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 12px;">Opacity Mask</td>
                <td style="padding: 12px;">Transparansi berbasis gradasi grayscale.</td>
            </tr>
            <tr>
                <td style="padding: 12px;">Gaussian Blur</td>
                <td style="padding: 12px;">Efek buram lembut untuk bayangan atau glow.</td>
            </tr>
        </table>

        <h2>Penutup</h2>
        <p>Di level ini, desainmu mulai "hidup". Warna bukan sekadar estetika, tetapi juga alat komunikasi visual. Dengan memahami teori warna, pencahayaan, dan teknik blending, kamu bisa menciptakan suasana, emosi, dan kedalaman hanya dari kombinasi warna yang tepat.</p>
        """,
        order=3
    )

    q5 = Question.objects.create(mission=m3, text="Apa fungsi dari Handle/Control Point pada Bezier curve?", order=1)
    Choice.objects.create(question=q5, text="Menentukan warna garis", is_correct=False)
    Choice.objects.create(question=q5, text="Menentukan bentuk lengkungan kurva", is_correct=True)
    Choice.objects.create(question=q5, text="Menentukan ketebalan garis", is_correct=False)
    Choice.objects.create(question=q5, text="Menentukan ukuran file", is_correct=False)

    q6 = Question.objects.create(mission=m3, text="Apa perbedaan antara Open Path dan Closed Path?", order=2)
    Choice.objects.create(question=q6, text="Open path berwarna, closed path tidak", is_correct=False)
    Choice.objects.create(question=q6, text="Open path titik awal dan akhirnya berbeda, closed path titik awal dan akhirnya bertemu", is_correct=True)
    Choice.objects.create(question=q6, text="Open path hanya bisa garis lurus", is_correct=False)
    Choice.objects.create(question=q6, text="Closed path tidak bisa diedit", is_correct=False)

    # ===== MISI 4: Typography Vektor =====
    m4 = Mission.objects.create(
        title="Master of Illustration (Ekspresi Visual)",
        description="Dari sketsa kasar, lahir karakter yang bernyawa.",
        xp_reward=100,
        content="""
        <h2>Materi Utama</h2>
        <h3>1. Alur Kerja Ilustrasi Digital (Raster → Vektor)</h3>
        <p>Proses ilustrasi sering dimulai dari sketsa bebas, lalu dirapikan menjadi vektor.</p>
        <ul>
            <li>Sketsa awal (raster): Bisa dibuat di kertas atau aplikasi digital.</li>
            <li>Import ke software vektor: Masukkan sketsa sebagai referensi.</li>
            <li>Tracing ulang: Gunakan Pen Tool atau Brush Tool untuk mengikuti bentuk sketsa.</li>
            <li>Konversi ke path bersih: Rapikan node dan kurva agar hasil presisi dan scalable.</li>
        </ul>
        <p>Alur ini menggabungkan kebebasan menggambar dengan presisi vektor.</p>

        <h3>2. Brushing Digital pada Vektor</h3>
        <p>Untuk gaya yang lebih ekspresif, gunakan teknik brush.</p>
        <ul>
            <li>Gunakan brush dengan pressure sensitivity (jika memakai tablet) untuk variasi ketebalan garis.</li>
            <li>Manfaatkan custom brush untuk efek alami seperti rambut, bulu, atau tekstur organik.</li>
        </ul>
        <p>Teknik ini membuat ilustrasi terasa lebih hidup dan tidak kaku.</p>

        <h3>3. Pembuatan Tekstur untuk Kesan Organik</h3>
        <p>Vektor cenderung terlalu "bersih". Tekstur membantu memberi karakter.</p>
        <ul>
            <li>Grain / noise / paper texture dengan kombinasi Opacity Mask dan Blending Mode.</li>
            <li>Menggunakan raster texture yang di-embed ke dalam desain vektor.</li>
        </ul>
        <p>Tekstur memberikan kedalaman visual dan nuansa realistis.</p>

        <h2>Konsep Kunci</h2>
        <table style="width:100%; border-collapse: collapse; margin: 16px 0;">
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                <th style="padding: 12px; text-align: left; color: #818cf8;">Istilah</th>
                <th style="padding: 12px; text-align: left; color: #818cf8;">Penjelasan</th>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 12px;">Digital Inking</td>
                <td style="padding: 12px;">Proses membuat garis tegas pada sketsa menggunakan Brush Tool atau Pen Tool.</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 12px;">Layering Strategy</td>
                <td style="padding: 12px;">Pengelompokan layer (sketsa, ink, base color, shading, texture, background) untuk memudahkan revisi.</td>
            </tr>
            <tr>
                <td style="padding: 12px;">Symbol Sprayer</td>
                <td style="padding: 12px;">Alat untuk menyemprotkan simbol berulang secara acak namun terkontrol.</td>
            </tr>
        </table>

        <h2>Penutup</h2>
        <p>Pada level ini, kamu mulai menciptakan karya yang benar-benar personal. Dari sketsa kasar hingga ilustrasi jadi, setiap garis dan tekstur mencerminkan gaya unikmu. Inilah tahap di mana teknik bertemu ekspresi—dan desain berubah menjadi karya seni.</p>
        """,
        order=4
    )

    q7 = Question.objects.create(mission=m4, text="Apa yang dimaksud dengan 'Convert to Outlines/Curves' pada teks?", order=1)
    Choice.objects.create(question=q7, text="Mengubah warna teks", is_correct=False)
    Choice.objects.create(question=q7, text="Mengubah teks menjadi path vektor yang bisa dimanipulasi bentuknya", is_correct=True)
    Choice.objects.create(question=q7, text="Menghapus teks dari desain", is_correct=False)
    Choice.objects.create(question=q7, text="Membuat teks menjadi 3D", is_correct=False)

    q8 = Question.objects.create(mission=m4, text="Apa perbedaan antara Kerning dan Tracking?", order=2)
    Choice.objects.create(question=q8, text="Kerning untuk jarak antar baris, Tracking untuk jarak antar huruf", is_correct=False)
    Choice.objects.create(question=q8, text="Kerning untuk jarak antar karakter individual, Tracking untuk jarak keseluruhan antar huruf", is_correct=True)
    Choice.objects.create(question=q8, text="Keduanya sama saja", is_correct=False)
    Choice.objects.create(question=q8, text="Kerning untuk ukuran huruf, Tracking untuk warna huruf", is_correct=False)

    # ===== MISI 5: Ekspor dan Format File Vektor =====
    m5 = Mission.objects.create(
        title="Industry Ready (Produksi & Finalisasi)",
        description="Karya yang hebat tidak cukup; harus siap dikirim ke klien.",
        xp_reward=100,
        content="""
        <h2>Materi Utama</h2>
        <h3>1. Finalisasi Aset untuk Berbagai Kebutuhan</h3>
        <p>Setiap media memiliki standar teknis yang berbeda, jadi desain harus disesuaikan sebelum dikirim.</p>
        <p><strong>Cetak (baliho, poster, dll.)</strong></p>
        <ul>
            <li>Mode warna CMYK</li>
            <li>Resolusi tinggi (umumnya 300 DPI)</li>
            <li>Tambahkan bleed untuk area potong</li>
            <li>Format umum: .eps, .pdf</li>
        </ul>
        <p><strong>Web / Antarmuka Digital</strong></p>
        <ul>
            <li>Mode warna RGB</li>
            <li>Ukuran file ringan</li>
            <li>Format: .svg, .webp</li>
            <li>Desain responsif (menyesuaikan layar)</li>
        </ul>
        <p><strong>Media Sosial</strong></p>
        <ul>
            <li>Format persegi (1:1) atau vertikal (4:5 / 9:16)</li>
            <li>Perhatikan batas ukuran file tiap platform</li>
            <li>Optimasi agar tetap tajam tapi ringan</li>
        </ul>

        <h3>2. Pembersihan Jalur (Cleaning Paths)</h3>
        <p>Desain profesional bukan hanya bagus dilihat, tapi juga rapi secara struktur.</p>
        <ul>
            <li>Hapus node yang tidak perlu (biar ringan)</li>
            <li>Gabungkan path yang identik</li>
            <li>Rapikan kurva agar smooth</li>
            <li>Ubah teks menjadi outline (hindari error font)</li>
        </ul>

        <h3>3. Manajemen File Profesional</h3>
        <p>File yang rapi = kerja cepat + klien percaya.</p>
        <p><strong>Penamaan:</strong></p>
        <ul>
            <li>Layer: logo_primary, background_shadow, dll</li>
            <li>Artboard: IG_post_01, banner_web_home, dll</li>
        </ul>
        <p><strong>Struktur folder:</strong></p>
        <pre>
Project_Name/
├── Sketch/
├── Source/
├── Export/
├── Mockup/
└── Manual/
        </pre>

        <h2>Konsep Kunci</h2>
        <p>(Konsep kunci untuk level ini mencakup praktik terbaik produksi dan finalisasi.)</p>
        <ul>
            <li><strong>Standar untuk percetakan</strong></li>
            <li>Kompatibel dengan banyak software desain</li>
            <li>Bisa berisi vektor dan raster sekaligus</li>
        </ul>

        <h3>4. PDF (Portable Document Format)</h3>
        <ul>
            <li>Bisa menyimpan data vektor dengan sempurna</li>
            <li>Universal - bisa dibuka di hampir semua perangkat</li>
            <li>Cocok untuk print dan distribusi digital</li>
        </ul>

        <h3>5. CDR (CorelDRAW)</h3>
        <ul>
            <li>Format native CorelDRAW</li>
            <li>Populer di Indonesia untuk percetakan</li>
            <li>Hanya bisa dibuka sempurna di CorelDRAW</li>
        </ul>

        <h3>Panduan Ekspor</h3>
        <table style="width:100%; border-collapse: collapse; margin: 16px 0;">
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                <th style="padding: 12px; text-align: left; color: #818cf8;">Kebutuhan</th>
                <th style="padding: 12px; text-align: left; color: #818cf8;">Format</th>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 12px;">Website / Aplikasi</td>
                <td style="padding: 12px;">SVG</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 12px;">Cetak profesional</td>
                <td style="padding: 12px;">EPS atau PDF</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 12px;">Kolaborasi tim desain</td>
                <td style="padding: 12px;">AI atau CDR</td>
            </tr>
            <tr>
                <td style="padding: 12px;">Sharing universal</td>
                <td style="padding: 12px;">PDF</td>
            </tr>
        </table>

        <h3>Tips Ekspor</h3>
        <ul>
            <li>Selalu simpan file sumber (AI/CDR) sebelum mengekspor ke format lain</li>
            <li>Convert text to outlines sebelum ekspor untuk menghindari masalah font</li>
            <li>Untuk web, optimasi SVG dengan tools seperti SVGO</li>
            <li>Untuk cetak, pastikan color mode CMYK dan resolusi minimal 300 DPI</li>
        </ul>
        """,
        order=5
    )

    q9 = Question.objects.create(mission=m5, text="Format vektor apa yang paling ideal untuk digunakan di website?", order=1)
    Choice.objects.create(question=q9, text="AI", is_correct=False)
    Choice.objects.create(question=q9, text="EPS", is_correct=False)
    Choice.objects.create(question=q9, text="SVG", is_correct=True)
    Choice.objects.create(question=q9, text="CDR", is_correct=False)

    q10 = Question.objects.create(mission=m5, text="Apa yang harus dilakukan sebelum mengekspor file vektor ke percetakan?", order=2)
    Choice.objects.create(question=q10, text="Mengubah ke format GIF", is_correct=False)
    Choice.objects.create(question=q10, text="Convert text to outlines dan pastikan color mode CMYK", is_correct=True)
    Choice.objects.create(question=q10, text="Menghapus semua layer", is_correct=False)
    Choice.objects.create(question=q10, text="Mengubah resolusi ke 72 DPI", is_correct=False)

    print("5 misi gambar vektor berhasil ditambahkan!")
    print(f"   Total misi: {Mission.objects.count()}")
    print(f"   Total soal: {Question.objects.count()}")
    print(f"   Total pilihan: {Choice.objects.count()}")

    # ===== COMMUNITY ROOMS =====
    CommunityRoom.objects.all().delete()
    
    room1 = CommunityRoom.objects.create(
        name="Room Diskusi Vektor Dasar",
        token="VEKTOR101",
        content='<h3>Pertanyaan Kuis: Apa itu gambar vektor?</h3><p>Jawablah pertanyaan berikut dengan benar untuk mendapatkan poin tambahan!</p><ol><li>Gambar vektor adalah gambar yang terdiri dari piksel-piksel.</li><li>Gambar vektor dapat diperbesar tanpa kehilangan kualitas.</li><li>Gambar vektor cocok untuk foto dengan detail kompleks.</li><li>Gambar vektor berbasis matematika dan garis.</li></ol><p><strong>Jawaban yang benar:</strong> 2 dan 4</p>'
    )
    
    room2 = CommunityRoom.objects.create(
        name="Room Tantangan Desain",
        token="DESIGN202",
        content='<h3>Kuis Mini: Teknik Bezier Curve</h3><p>Uji pengetahuanmu tentang Bezier curve!</p><p><strong>Pertanyaan:</strong> Apa fungsi dari anchor point pada Bezier curve?</p><ul><li>A. Menentukan warna kurva</li><li>B. Menentukan titik awal dan akhir kurva</li><li>C. Menentukan ketebalan garis</li><li>D. Menentukan ukuran file</li></ul><p><strong>Jawaban:</strong> B. Menentukan titik awal dan akhir kurva</p><p><strong>Penjelasan:</strong> Anchor point adalah titik kontrol utama yang menentukan posisi awal dan akhir dari sebuah path atau kurva.</p>'
    )
    
    print("2 community rooms berhasil ditambahkan!")
    print(f"   Room 1: {room1.name} - Token: {room1.token}")
    print(f"   Room 2: {room2.name} - Token: {room2.token}")

if __name__ == '__main__':
    run()
