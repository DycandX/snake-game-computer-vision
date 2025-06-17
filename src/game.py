import cv2
import random
import math
import cvzone
import numpy as np

class SnakeGameClass:
    def __init__(self, pathFood, snake_head_img, eat_sound, game_over_sound):  # Menambahkan game_over_sound sebagai parameter
        self.points = []  # Posisi kepala dan tubuh ular
        self.lengths = []  # Panjang antara setiap titik tubuh ular
        self.currentLength = 0  # Panjang total ular
        self.allowedLength = 150  # Panjang ular yang diizinkan
        self.previousHead = 0, 0  # Titik sebelumnya dari kepala ular
        self.score = 0  # Skor permainan
        self.gameOver = False  # Status game over
        self.eat_sound = eat_sound  # Menyimpan objek eat_sound
        self.game_over_sound = game_over_sound  # Menyimpan objek game_over_sound

        # Muat gambar makanan
        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        if self.imgFood is None:
            print(f"Error: Unable to load image at {pathFood}")
            exit()

        self.hFood, self.wFood, _ = self.imgFood.shape
        self.foodPoint = 0, 0  # Titik posisi makanan
        self.randomFoodLocation()  # Tempatkan makanan di lokasi acak

        # Menyimpan gambar kepala ular
        self.snake_head_img = snake_head_img

    def randomFoodLocation(self):
        self.foodPoint = random.randint(100, 1000), random.randint(100, 600)

    def update(self, imgMain, currentHead):
        if self.gameOver:
            self.game_over_sound.play()  # Memainkan suara game over
            cvzone.putTextRect(imgMain, "Game Over", [500, 300], scale=4, thickness=5, offset=10)
            cvzone.putTextRect(imgMain, f'Your Score: {self.score}', [500, 370], scale=3, thickness=4, offset=10)
            cvzone.putTextRect(imgMain, "Press 'R' to Restart or 'M' for Main Menu", [320, 450], scale=2, thickness=3, offset=10)
        else:
            px, py = self.previousHead
            cx, cy = currentHead

            self.points.append([cx, cy])  # Menambahkan posisi kepala ular ke titik tubuh
            distance = math.hypot(cx - px, cy - py)  # Menghitung jarak antara posisi kepala dan tubuh
            self.lengths.append(distance)
            self.currentLength += distance
            self.previousHead = cx, cy

            # Length Reduction (memotong panjang ular jika terlalu panjang)
            if self.currentLength > self.allowedLength:
                for i, length in enumerate(self.lengths):
                    self.currentLength -= length
                    self.lengths.pop(i)
                    self.points.pop(i)
                    if self.currentLength < self.allowedLength:
                        break

            # Check if snake ate the food (memeriksa apakah ular makan makanan)
            rx, ry = self.foodPoint
            if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and \
                    ry - self.hFood // 2 < cy < ry + self.hFood // 2:
                self.randomFoodLocation()
                self.allowedLength += 50
                self.score += 1
                self.eat_sound.play()  # Memainkan suara makan

            # Gambar Snake (menggunakan gambar kepala ular)
            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv2.line(imgMain, self.points[i - 1], self.points[i], (0, 0, 255), 20)

            # Menampilkan gambar kepala ular di ujung telunjuk
            head_x, head_y = currentHead
            imgMain = cvzone.overlayPNG(imgMain, self.snake_head_img, (head_x - self.snake_head_img.shape[1] // 2, head_y - self.snake_head_img.shape[0] // 2))

            # Gambar makanan
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood, (rx - self.wFood // 2, ry - self.hFood // 2))

        # Selalu tampilkan skor
        cvzone.putTextRect(imgMain, f'Score: {self.score}', [50, 80], scale=3, thickness=3, offset=10)

        # Cek untuk Collision (deteksi tabrakan dengan tubuh ular)
        if not self.gameOver:
            pts = np.array(self.points[:-2], np.int32)  # Mengambil titik tubuh ular (kecuali kepala dan titik terakhir)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(imgMain, [pts], False, (0, 255, 0), 3)
            minDist = cv2.pointPolygonTest(pts, (currentHead[0], currentHead[1]), True)

            # Jika jarak antara kepala dan tubuh berada dalam batas tertentu, berarti terjadi tabrakan
            if -1 <= minDist <= 1:
                self.gameOver = True  # Game berakhir jika terjadi tabrakan
                self.points = []  # Reset titik tubuh ular
                self.lengths = []  # Reset panjang tubuh ular
                self.currentLength = 0  # Reset panjang total
                self.allowedLength = 150  # Reset panjang ular yang diizinkan
                self.previousHead = 0, 0  # Reset posisi kepala ular
                self.randomFoodLocation()

        return imgMain

    def reset_game(self):
        self.gameOver = False
        self.score = 0
        self.points = []
        self.lengths = []
        self.currentLength = 0
        self.allowedLength = 150
        self.previousHead = 0, 0
        self.randomFoodLocation()
