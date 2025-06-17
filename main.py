import pygame
import cv2
import random
import math
import numpy as np
import cvzone
from cvzone.HandTrackingModule import HandDetector
from utils import draw_button, draw_text

# Inisialisasi Pygame mixer untuk pemutaran audio
pygame.mixer.init()

# Muat file musik BGM dan efek suara
pygame.mixer.music.load("assets/sounds/BGM.wav")
eat_sound = pygame.mixer.Sound("assets/sounds/eat.wav")
game_over_sound = pygame.mixer.Sound("assets/sounds/game-over.wav")

# Setel volume BGM dan game over ke 15%
pygame.mixer.music.set_volume(0.15)  # Set volume BGM 15%
game_over_sound.set_volume(0.15)  # Set volume suara game over 15%

# Mulai memutar BGM secara berulang
pygame.mixer.music.play(-1, 0.0)  # -1 untuk pemutaran berulang, 0.0 untuk memulai dari awal

# Setup kamera dan deteksi tangan
cap = cv2.VideoCapture(3)
if not cap.isOpened():
    print("Error: Camera not found or not accessible.")
    exit()

cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=1)

# Muat gambar kepala ular
snake_head_img = cv2.imread("assets/images/SnakeHead.png", cv2.IMREAD_UNCHANGED)
if snake_head_img is None:
    print("Error: Unable to load SnakeHead.png")
    exit()

# Menentukan ukuran baru (misalnya 50% dari ukuran asli)
new_width = int(snake_head_img.shape[1] * 0.15)  # Setel lebar gambar menjadi 50% dari aslinya
new_height = int(snake_head_img.shape[0] * 0.15)  # Setel tinggi gambar menjadi 50% dari aslinya

# Mengubah ukuran gambar menggunakan cv2.resize
snake_head_img = cv2.resize(snake_head_img, (new_width, new_height))

# Muat gambar latar belakang menu dan ubah ukurannya
menu_img = cv2.imread("assets/images/menu.png")
if menu_img is None:
    print("Error: Unable to load menu.png")
    exit()

# Menyesuaikan ukuran gambar menu (misalnya, 70% dari ukuran asli)
menu_width = int(menu_img.shape[1] * 0.7)  # Setel lebar gambar menu menjadi 70% dari aslinya
menu_height = int(menu_img.shape[0] * 0.7)  # Setel tinggi gambar menu menjadi 70% dari aslinya

# Mengubah ukuran gambar menu menggunakan cv2.resize
menu_img = cv2.resize(menu_img, (menu_width, menu_height))


# Kelas Game Snake
class SnakeGameClass:
    def __init__(self, pathFood):
        self.points = []
        self.lengths = []
        self.currentLength = 0
        self.allowedLength = 150
        self.previousHead = 0, 0

        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        if self.imgFood is None:
            print(f"Error: Unable to load image at {pathFood}")
            exit()

        self.hFood, self.wFood, _ = self.imgFood.shape
        self.foodPoint = 0, 0
        self.randomFoodLocation()

        self.score = 0
        self.gameOver = False

    def randomFoodLocation(self):
        self.foodPoint = random.randint(100, 1000), random.randint(100, 600)

    def update(self, imgMain, currentHead):
        if self.gameOver:
            game_over_sound.play()

            cvzone.putTextRect(imgMain, "Game Over", [500, 300], scale=4, thickness=5, offset=10)
            cvzone.putTextRect(imgMain, f'Your Score: {self.score}', [500, 370], scale=3, thickness=4, offset=10)
            cvzone.putTextRect(imgMain, "Press 'R' to Restart or 'M' for Main Menu", [320, 450], scale=2, thickness=3,
                               offset=10)
        else:
            px, py = self.previousHead
            cx, cy = currentHead

            self.points.append([cx, cy])
            distance = math.hypot(cx - px, cy - py)
            self.lengths.append(distance)
            self.currentLength += distance
            self.previousHead = cx, cy

            # Length Reduction
            if self.currentLength > self.allowedLength:
                for i, length in enumerate(self.lengths):
                    self.currentLength -= length
                    self.lengths.pop(i)
                    self.points.pop(i)
                    if self.currentLength < self.allowedLength:
                        break

            # Check if snake ate the food
            rx, ry = self.foodPoint
            if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and \
                    ry - self.hFood // 2 < cy < ry + self.hFood // 2:
                self.randomFoodLocation()
                self.allowedLength += 50
                self.score += 1
                eat_sound.play()

            # Gambar Snake (menggunakan gambar kepala ular)
            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv2.line(imgMain, self.points[i - 1], self.points[i], (0, 0, 255), 20)

            # Menampilkan gambar kepala ular di ujung telunjuk
            head_x, head_y = currentHead
            imgMain = cvzone.overlayPNG(imgMain, snake_head_img,
                                        (head_x - snake_head_img.shape[1] // 2, head_y - snake_head_img.shape[0] // 2))

            # Gambar makanan
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood, (rx - self.wFood // 2, ry - self.hFood // 2))

        # Selalu tampilkan skor
        cvzone.putTextRect(imgMain, f'Score: {self.score}', [50, 80], scale=3, thickness=3, offset=10)

        # Cek untuk Collision
        if not self.gameOver:
            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(imgMain, [pts], False, (0, 255, 0), 3)
            minDist = cv2.pointPolygonTest(pts, (currentHead[0], currentHead[1]), True)

            if -1 <= minDist <= 1:
                self.gameOver = True
                self.points = []
                self.lengths = []
                self.currentLength = 0
                self.allowedLength = 150
                self.previousHead = 0, 0
                self.randomFoodLocation()

        return imgMain


# Menu Utama
def main_menu():
    while True:
        img = menu_img.copy()  # Salin gambar menu.png sebagai latar belakang

        # Menempatkan teks di tengah layar
        # text = "Snake Game"
        # text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 3, 3)[0]
        # text_x = (menu_img.shape[1] - text_size[0]) // 2
        # text_y = 100  # Posisi vertikal di atas
        # draw_text(img, text, [text_x, text_y], scale=3)

        # Gambar tombol di tengah layar tanpa border
        button_width = 300
        button_height = 50
        start_button = draw_button(img, "Start Game (S)", [(menu_img.shape[1] - button_width) // 2, 400], button_width,
                                   button_height)
        exit_button = draw_button(img, "Exit (Q)", [(menu_img.shape[1] - button_width) // 2, 500], button_width,
                                  button_height)

        # Tampilkan menu
        cv2.imshow("Snake Game", img)

        # Deteksi interaksi tangan dengan tombol
        hands, img = detector.findHands(img, flipType=False)

        if hands:
            lmList = hands[0]['lmList']
            pointIndex = lmList[8][0:2]

            # Periksa apakah jari menunjuk ke tombol
            if is_point_in_rect(pointIndex, start_button):
                return "start"
            elif is_point_in_rect(pointIndex, exit_button):
                cv2.destroyAllWindows()
                exit()

        # Tunggu input tombol atau interaksi tangan
        key = cv2.waitKey(1)
        if key == ord('s') or key == ord('S'):
            return "start"
        elif key == ord('q') or key == ord('Q'):
            cv2.destroyAllWindows()
            exit()


def is_point_in_rect(point, rect):
    x, y = point
    x1, y1, x2, y2 = rect
    return x1 <= x <= x2 and y1 <= y <= y2


# Inisialisasi game
game = SnakeGameClass("assets/images/Donut.png")

while True:
    menu_action = main_menu()

    if menu_action == "start":
        while True:
            success, img = cap.read()
            if not success:
                print("Error: Unable to read from camera")
                break

            img = cv2.flip(img, 1)
            hands, img = detector.findHands(img, flipType=False)

            if hands:
                lmList = hands[0]['lmList']
                pointIndex = lmList[8][0:2]
                img = game.update(img, pointIndex)

            cv2.imshow("Snake Game", img)

            key = cv2.waitKey(1)

            if key == ord('r') or key == ord('R'):  # Restart game on pressing 'R'
                game.gameOver = False
                game.score = 0
                game.points = []
                game.lengths = []
                game.currentLength = 0
                game.allowedLength = 150
                game.previousHead = 0, 0
                game.randomFoodLocation()

            elif key == ord('m') or key == ord('M'):  # Return to main menu on pressing 'M'
                cv2.destroyWindow("Snake Game")
                break

cap.release()
cv2.destroyAllWindows()
