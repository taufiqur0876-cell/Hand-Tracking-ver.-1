# Hand Tracking Gesture Recognition with Text-to-Speech (TTS)

Sebuah proyek berbasis visi komputer (*computer vision*) dan kecerdasan buatan (*artificial intelligence*) yang mendeteksi posisi jari tangan secara *real-time* menggunakan kamera (Webcam) untuk memetakan gerakan tangan (*gesture*) menjadi perintah suara teks-ke-bicara (*Text-to-Speech*).

Proyek ini sangat berguna untuk membantu interaksi manusia dan komputer yang lebih interaktif, serta berpotensi dikembangkan sebagai alat bantu komunikasi non-verbal (bahasa isyarat).

---

## 🚀 Fitur Utama

1. **Deteksi Tangan Presisi Tinggi**: Menggunakan algoritma mutakhir Google MediaPipe Hands untuk melacak 21 titik koordinat (*landmarks*) tangan secara *real-time*.
2. **Text-to-Speech (TTS) Terintegrasi**: Menggunakan pustaka `pyttsx3` untuk mengonversi hasil deteksi menjadi ucapan suara bahasa Indonesia yang natural secara dinamis.
3. **Penyaringan Cooldown Suara**: Sistem dilengkapi dengan kontrol jeda (*cooldown*) waktu untuk mencegah penumpukan suara (*overlapping*) saat deteksi berlangsung terus-menerus.
4. **Fleksibilitas Platform (Multiplatform)**: Dapat dijalankan langsung di mesin lokal atau diisolasi menggunakan **Docker** guna memastikan kompatibilitas sistem operasi terjamin 100%.

---

## 🛠️ Pemetaan Isyarat & Perintah Suara

Sistem saat ini mendukung tiga logika pengenalan isyarat tangan utama:

| No | Gerakan Jari (Gesture) | Arti Visual di Layar | Output Suara (TTS) |
|---|---|---|---|
| 1 | Jari Telunjuk & Jari Tengah Naik (Peace/V) | "Perintah: Teman" | "Teman" |
| 2 | Hanya Jari Telunjuk yang Naik | "Perintah: Halo" | "Halo" |
| 3 | Hanya Jari Tengah yang Naik | "Perintah: Cinta" | "Cinta" |

---

## 📂 Struktur Repositori

```text
Hand-Tracking-ver.-1/
├── main.py               # Kode utama aplikasi
├── requirements.txt      # Daftar pustaka (dependencies) Python
├── Dockerfile            # Cetak biru Docker untuk isolasi environment
└── README.md             # Dokumentasi proyek (File ini)
```

---

## ⚙️ Persyaratan Sistem & Instalasi

### Metode 1: Menjalankan di Mesin Lokal (Lokal Environment)

**1. Pastikan Python sudah terinstal (Direkomendasikan Python 3.10+)**

**2. Kloning atau unduh repositori ini, lalu masuk ke foldernya:**
```bash
cd Hand-Tracking-ver.-1
```

**3. Pasang semua pustaka yang diperlukan:**
Kami merekomendasikan penggunaan lingkungan virtual (*virtual environment*) agar tidak mengotori sistem global Anda:
```bash
# Membuat virtual environment (opsional)
python -m venv venv
source venv/bin/activate  # Untuk Linux/Mac
# atau
.\\venv\\Scripts\\activate  # Untuk Windows

# Instalasi dependencies mendasar
pip install opencv-python==4.8.0.76 mediapipe==0.10.9 pyttsx3==2.99 numpy==1.26.2
```
*(Catatan: `requirements.txt` lengkap telah disediakan untuk instalasi sekali jalan menggunakan `pip install -r requirements.txt`)*

**4. Jalankan aplikasi:**
```bash
python main.py
```

---

### Metode 2: Menggunakan Docker (Sangat Direkomendasikan)

Jika Anda ingin menghindari masalah konfigurasi pustaka eksternal (terutama pustaka grafis OpenGL yang diperlukan oleh OpenCV dan MediaPipe), Docker adalah solusi terbaik.

**1. Bangun Image Docker:**
```bash
docker build -t hand-tracking-app .
```

**2. Jalankan Container dengan Akses Kamera (Webcam):**
*   **Untuk pengguna Linux:**
    ```bash
    docker run --device=/dev/video0 hand-tracking-app
    ```
*   **Untuk pengguna Windows/Mac (melalui WSL2 atau Docker Desktop):**
    Pastikan Anda mengaktifkan dukungan pemetaan perangkat USB Webcam ke dalam Docker menggunakan alat pembantu seperti `usbipd` pada Windows.

---

## 💻 Penjelasan Kode Inti (`main.py`)

Alur logika aplikasi ini bekerja secara sekuensial dalam satu siklus *looping* gambar:
1. **Penerimaan Frame**: Gambar diambil dari webcam menggunakan `cv2.VideoCapture`.
2. **Pra-pemrosesan**: Gambar dibalik (*flipped*) agar berfungsi seperti cermin, lalu ruang warna dikonversi dari BGR (bawaan OpenCV) ke RGB (bawaan MediaPipe).
3. **Deteksi Posisi Jari**: Melalui fungsi pembantu `is_finger_up()`, aplikasi membandingkan nilai koordinat Y ujung jari dengan ruas jari di bawahnya. Pada layar komputer, sumbu Y bernilai semakin besar ke arah bawah. Oleh karena itu, jika nilai koordinat Y ujung jari lebih kecil dari nilai Y ruas bawah, maka jari tersebut disimpulkan sedang **NAIK**.
4. **Sintesis Suara**: Engine `pyttsx3` memproses string perintah terpilih dan mengonversinya menjadi ucapan audio dengan penanganan jeda waktu (*cooldown*) berbasis modul `time`.

---

## 📄 Lisensi
Proyek ini dilisensikan di bawah Lisensi MIT. Anda bebas menggunakan, memodifikasi, dan mendistribusikan kode ini untuk tujuan akademis maupun komersial.
