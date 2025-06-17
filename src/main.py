import pygame
import cv2
from game import SnakeGameClass
from menu import main_menu
from hand_detection import HandDetector
import random

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

# Menentukan ukuran baru gambar kepala ular
new_width = int(snake_head_img.shape[1] * 0.15)
new_height = int(snake_head_img.shape[0] * 0.15)
snake_head_img = cv2.resize(snake_head_img, (new_width, new_height))

# Muat gambar Donut dan cek apakah berhasil dimuat
donut_img = cv2.imread("assets/images/Donut.png", cv2.IMREAD_UNCHANGED)
if donut_img is None:
    print("Error: Unable to load Donut.png")
    exit()

# Menyesuaikan ukuran gambar menu
menu_img = cv2.imread("assets/images/menu.png")
if menu_img is None:
    print("Error: Unable to load menu.png")
    exit()

menu_width = int(menu_img.shape[1] * 0.7)
menu_height = int(menu_img.shape[0] * 0.7)
menu_img = cv2.resize(menu_img, (menu_width, menu_height))

# Inisialisasi game, pass game_over_sound ke SnakeGameClass
game = SnakeGameClass("assets/images/Donut.png", snake_head_img, eat_sound, game_over_sound)

while True:
    menu_action = main_menu(menu_img, detector)  # Pass the menu image and detector
    if menu_action == "start":
        while True:
            success, img = cap.read()
            if not success:
                print("Error: Unable to read from camera")
                break

            img = cv2.flip(img, 1)  # Flip the image horizontally
            hands, img = detector.findHands(img, flipType=False)

            if hands:
                lmList = hands[0]['lmList']
                pointIndex = lmList[8][0:2]
                img = game.update(img, pointIndex)

            cv2.imshow("Snake Game", img)

            key = cv2.waitKey(1)
            if key == ord('r') or key == ord('R'):  # Restart game
                game.reset_game()
            elif key == ord('m') or key == ord('M'):  # Return to main menu
                cv2.destroyWindow("Snake Game")
                break

cap.release()
cv2.destroyAllWindows()
