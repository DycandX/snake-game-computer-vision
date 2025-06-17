Tentu! Berikut adalah file **`README.md`** yang bisa Anda salin dan tempel ke dalam proyek Anda.

### **README.md**

````markdown
# Snake Game with Hand Detection

## Deskripsi
Snake Game dengan **deteksi tangan** menggunakan **OpenCV** dan **pygame**. Dalam game ini, pemain mengontrol ular dengan gerakan tangan (menggunakan deteksi jari telunjuk) dan bertujuan untuk makan makanan yang muncul di layar, meningkatkan skor. Game akan berakhir ketika kepala ular bertabrakan dengan tubuhnya.

## Fitur
- Deteksi gerakan tangan menggunakan **OpenCV** dan **cvzone**.
- Pemain menggerakkan ular menggunakan jari telunjuk yang terdeteksi oleh kamera.
- Suara latar belakang (BGM), efek suara makan makanan, dan suara **game over**.
- Tampilan menu utama dengan tombol **Start** dan **Exit**.
- Fitur game over dan restart permainan.
- Tampilan skor yang selalu terlihat selama permainan.

## Teknologi yang Digunakan
- **Python 3.x**
- **pygame**: Untuk pemutaran audio dan pengaturan game.
- **OpenCV**: Untuk pemrosesan citra dan deteksi tangan.
- **cvzone**: Untuk menambahkan teks dan overlay pada gambar.
- **NumPy**: Untuk pengolahan array dan deteksi tabrakan.

## Persyaratan
Pastikan Anda telah menginstal semua dependensi berikut:

```bash
pip install pygame opencv-python cvzone numpy
````

## Instalasi

1. **Clone repositori ini**:

   ```bash
   git clone https://github.com/username/SnakeGameCamera.git
   ```

2. **Masuk ke direktori proyek**:

   ```bash
   cd SnakeGameCamera
   ```

3. **Instal dependensi yang diperlukan**:

   ```bash
   pip install pygame opencv-python cvzone numpy
   ```

4. **Jalankan program**:

   ```bash
   python src/main.py
   ```

## Penggunaan

1. **Menu Utama**:

   * Tekan **'S'** untuk memulai permainan.
   * Tekan **'Q'** untuk keluar dari permainan.

2. **Kontrol**:

   * Gunakan **jari telunjuk** untuk menggerakkan ular.
   * Ular akan bergerak mengikuti posisi jari telunjuk yang terdeteksi oleh kamera.

3. **Game Over**:

   * Permainan akan berakhir ketika kepala ular bertabrakan dengan tubuhnya.
   * Tekan **'R'** untuk memulai ulang permainan.
   * Tekan **'M'** untuk kembali ke menu utama.

## Struktur Proyek

```bash
/SnakeGameCamera
│
├── /assets
│   ├── /sounds
│   │   ├── BGM.wav
│   │   ├── eat.wav
│   │   └── game-over.wav
│   └── /images
│       ├── Donut.png
│       ├── SnakeHead.png
│       └── menu.png
│
├── /src
│   ├── main.py
│   ├── game.py
│   ├── menu.py
│   ├── hand_detection.py
│   └── utils.py
│
└── README.md
```

### Penjelasan Struktur Proyek:

1. **`/assets/sounds/`**: Berisi file audio untuk BGM, efek suara makan makanan, dan suara game over.
2. **`/assets/images/`**: Berisi gambar untuk makanan (Donut), kepala ular (SnakeHead), dan menu utama (menu.png).
3. **`/src/`**: Berisi kode utama program, termasuk logika permainan, menu, deteksi tangan, dan utilitas tambahan.

   * **`main.py`**: Berisi kode utama untuk menjalankan permainan.
   * **`game.py`**: Menangani logika permainan Snake, seperti deteksi makanan, pergerakan ular, dan tabrakan.
   * **`menu.py`**: Menangani tampilan menu utama dan interaksi tombol.
   * **`hand_detection.py`**: Menangani deteksi tangan menggunakan **cvzone** dan **OpenCV**.
   * **`utils.py`**: Berisi fungsi utilitas untuk menggambar tombol dan teks pada layar.

## Kontribusi

Jika Anda ingin berkontribusi pada proyek ini, silakan lakukan **fork** repositori ini dan buat **pull request** setelah melakukan perubahan. Pastikan untuk mengikuti konvensi dan format kode yang ada.

## Lisensi

Proyek ini dilisensikan di bawah **MIT License** - lihat file [LICENSE](LICENSE) untuk detail lebih lanjut.
