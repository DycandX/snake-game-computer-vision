
# Snake Game dengan Computer Vision

Proyek ini adalah **Snake Game** di mana pergerakan ular dikendalikan dengan gerakan tangan menggunakan kamera, dengan memanfaatkan teknik **Computer Vision**. Permainan ini diimplementasikan menggunakan **OpenCV** untuk pengolahan citra, **Pygame** untuk efek suara, dan **cvzone** untuk pelacakan tangan.

## Fitur

- **Pelacakan Tangan**: Pergerakan ular dikendalikan dengan mendeteksi tangan pengguna menggunakan kamera. Permainan ini menggunakan **HandTrackingModule** dari **cvzone** untuk mendeteksi dan melacak posisi jari telunjuk.
- **Suara Permainan**: Permainan ini memiliki musik latar belakang (**BGM**) dan efek suara untuk makan makanan dan peristiwa game over.
- **Deteksi Tabrakan**: Permainan ini menerapkan sistem deteksi tabrakan di mana permainan berakhir jika kepala ular bertabrakan dengan tubuhnya.
- **Interaksi Makanan**: Ular memakan makanan yang muncul secara acak di layar. Setiap kali ular memakan makanan, panjang ular bertambah dan skor diperbarui.

## Persyaratan

- Python 3.10
- Pygame
- OpenCV
- cvzone

## Instalasi

1. Clone repositori ini:
   ```bash
   https://github.com/DycandX/snake-game-computer-vision.git


2. Instal dependensi yang diperlukan:

   ```bash
   pip install -r requirements.txt
   ```

3. Pastikan Anda memiliki file-file berikut di folder **`/assets`**:

   * **`/assets/sounds/BGM.wav`** (Musik latar belakang)
   * **`/assets/sounds/eat.wav`** (Efek suara untuk makan makanan)
   * **`/assets/sounds/game-over.wav`** (Efek suara untuk game over)
   * **`/assets/images/SnakeHead.png`** (Gambar kepala ular)
   * **`/assets/images/Donut.png`** (Gambar makanan)
   * **`/assets/images/menu.png`** (Gambar untuk layar menu)

4. Jalankan permainan:

   ```bash
   python src/main.py
   ```

## Cara Kerja

* **Kontrol Gerakan Tangan**: Permainan ini menggunakan kamera untuk mendeteksi tangan pengguna. Posisi jari telunjuk dilacak, dan ular mengikuti gerakan tersebut. Deteksi jari telunjuk dilakukan dengan menggunakan **cvzone.HandTrackingModule**.

* **Mekanisme Permainan**:

  * Ular bergerak sesuai dengan posisi jari telunjuk.
  * Ketika ular memakan makanan, panjangnya bertambah dan skor meningkat.
  * Jika ular bertabrakan dengan tubuhnya sendiri, permainan berakhir dan suara game over dimainkan.
  * Pengguna dapat memulai ulang permainan dengan menekan **'R'** atau kembali ke menu utama dengan menekan **'M'**.

* **Layar Menu**: Permainan dimulai dengan menu di mana pengguna dapat memilih untuk **memulai** permainan dengan menekan **'S'** atau keluar dengan menekan **'Q'**.

## Demo

\[soon]

## Kontributor

* **Nama**: Zulvikar Kharisma Nur Muhammad (4.33.23.2.26)
* **Mata Kuliah**: Pengolahan Citra
* **Dosen Pengampu**: Ir. Prayitno, S.ST., M.T., Ph.D


