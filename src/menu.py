import cvzone
import cv2
from utils import draw_button, draw_text


def main_menu(menu_img, detector):
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
