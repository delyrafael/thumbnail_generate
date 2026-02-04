Berikut adalah draf file `README.md` yang profesional dan lengkap untuk proyek **Pro YouTube Thumbnail Maker** Anda. File ini mencakup instruksi instalasi, fitur, dan cara penggunaan.

---

```markdown
# 🎬 Pro YouTube Thumbnail Maker (Rembg Edition)

Aplikasi berbasis Python untuk membuat thumbnail YouTube profesional secara otomatis dari video. Alat ini menggunakan AI untuk menghapus background subjek dan menggabungkannya dengan collage background dari scene video lainnya.

## ✨ Fitur Utama
* **AI Background Removal**: Menggunakan library `rembg` untuk memisahkan subjek dari background secara instan.
* **Automatic Collage**: Membuat background grid 2x2 secara otomatis dari potongan-potongan frame video.
* **YouTube Style Typography**: Menambahkan headline dengan gaya "Edukasi/Opini" YouTube (teks putih dengan box merah).
* **Interactive Frame Selection**: Pengguna bisa memilih 1 dari 8 frame yang diekstrak dari video untuk dijadikan subjek utama.
* **User-Friendly UI**: Dibangun menggunakan Gradio untuk antarmuka web yang sederhana.

## 🛠️ Prasyarat (Requirements)
Pastikan Anda sudah menginstal Python 3.9+ dan library berikut:

```bash
pip install gradio opencv-python numpy pillow rembg

```

## 🚀 Cara Menjalankan

1. Simpan kode ke dalam file bernama `postermalaka.py`.
2. Jalankan aplikasi melalui terminal:
```bash
python postermalaka.py

```


3. Buka link lokal yang muncul di terminal (biasanya `http://127.0.0.1:7860`).

## 📖 Cara Penggunaan

1. **Upload Video**: Masukkan file video yang ingin diambil frame-nya.
2. **Pilih Frame**: Sistem akan mengekstrak 8 frame secara otomatis. Klik pada salah satu gambar di galeri yang ingin dijadikan subjek utama (orang).
3. **Input Headline**: Masukkan teks menarik untuk thumbnail Anda.
4. **Generate**: Klik tombol **🚀 Generate Thumbnail** dan tunggu AI bekerja menghapus background dan menyusun komposisi gambar.

## 📂 Struktur Kode

* `ProThumbnailRembg`: Class utama yang menangani pemrosesan gambar (remove bg, collage, dan penulisan teks).
* `process_video()`: Fungsi untuk mengambil 8 sampel frame dari durasi video secara proporsional.
* `generate()`: Fungsi handler untuk merakit semua komponen menjadi hasil akhir.
* `gr.Blocks`: Definisi antarmuka pengguna (UI) menggunakan Gradio.

## ⚙️ Kustomisasi Font

Aplikasi ini mencoba mencari font `arialbd.ttf` (Arial Bold) di sistem Windows. Jika Anda menggunakan Linux atau macOS, silakan ubah path font pada baris berikut di dalam class `__init__`:

```python
self.font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" # Contoh Linux

```

## 📝 Catatan

* Saat menjalankan pertama kali, library `rembg` akan mengunduh model AI (u2net) secara otomatis sebesar ~170MB.
* Hasil thumbnail memiliki resolusi standar YouTube yaitu **1280x720 (720p)**.

---

Dikembangkan dengan ❤️ menggunakan Gradio & Rembg.

```

---

### Tips Tambahan untuk Anda:
Jika Anda ingin menyertakan file ini di dalam folder proyek Anda, cukup buat file baru bernama `README.md` dan tempelkan (paste) teks di atas ke dalamnya.

**Apakah Anda ingin saya menambahkan bagian "Troubleshooting" atau instruksi cara menjalankan aplikasi ini menggunakan Docker?**

```
