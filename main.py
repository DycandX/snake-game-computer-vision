import math
import random
import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from utils import draw_button, draw_text  # Correct import for draw_text

# Try using the default camera (index 0)
cap = cv2.VideoCapture(2)  # Use default camera (index 0)
if not cap.isOpened():  # Check if the camera is successfully opened
    print("Error: Camera not found or not accessible.")
    exit()  # Exit if the camera cannot be accessed

cap.set(3, 1280)  # Set width
cap.set(4, 720)  # Set height

detector = HandDetector(detectionCon=0.8, maxHands=1)


class SnakeGameClass:
    def __init__(self, pathFood):
        self.points = []  # all points of the snake
        self.lengths = []  # distance between each point
        self.currentLength = 0  # total length of the snake
        self.allowedLength = 150  # total allowed Length
        self.previousHead = 0, 0  # previous head point

        # Load food image
        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        if self.imgFood is None:
            print(f"Error: Unable to load image at {pathFood}")
            exit()  # Exit if the image cannot be loaded

        self.hFood, self.wFood, _ = self.imgFood.shape
        self.foodPoint = 0, 0
        self.randomFoodLocation()

        self.score = 0
        self.gameOver = False

    def randomFoodLocation(self):
        self.foodPoint = random.randint(100, 1000), random.randint(100, 600)

    def update(self, imgMain, currentHead):
        if self.gameOver:
            # Adjust the font size and placement of the "Game Over" and score text
            cvzone.putTextRect(imgMain, "Game Over", [500, 300], scale=4, thickness=5, offset=10)
            cvzone.putTextRect(imgMain, f'Your Score: {self.score}', [500, 370], scale=3, thickness=4, offset=10)
            cvzone.putTextRect(imgMain, "Press 'R' to Restart or 'M' for Main Menu", [500, 450], scale=2, thickness=3,
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

            # Check if snake ate the Food
            rx, ry = self.foodPoint
            if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and \
                    ry - self.hFood // 2 < cy < ry + self.hFood // 2:
                self.randomFoodLocation()
                self.allowedLength += 50
                self.score += 1
                print(self.score)

            # Draw Snake
            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv2.line(imgMain, self.points[i - 1], self.points[i], (0, 0, 255), 20)
                cv2.circle(imgMain, self.points[-1], 20, (0, 255, 0), cv2.FILLED)

            # Draw Food
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood,
                                        (rx - self.wFood // 2, ry - self.hFood // 2))

        # Always show the score
        cvzone.putTextRect(imgMain, f'Score: {self.score}', [50, 80],
                           scale=3, thickness=3, offset=10)

        # Check for Collision
        if not self.gameOver:
            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(imgMain, [pts], False, (0, 255, 0), 3)
            minDist = cv2.pointPolygonTest(pts, (currentHead[0], currentHead[1]), True)

            if -1 <= minDist <= 1:
                print("Hit")
                self.gameOver = True
                self.points = []  # all points of the snake
                self.lengths = []  # distance between each point
                self.currentLength = 0  # total length of the snake
                self.allowedLength = 150  # total allowed Length
                self.previousHead = 0, 0  # previous head point
                self.randomFoodLocation()

        return imgMain


# Main Menu
def main_menu():
    while True:
        img = np.zeros((720, 1280, 3), np.uint8)
        draw_text(img, "Snake Game", [500, 100], scale=3)

        # Draw the buttons
        start_button = draw_button(img, "Start Game (S)", [500, 300], 300, 50)
        exit_button = draw_button(img, "Exit (Q)", [500, 500], 300, 50)

        # Show the menu
        cv2.imshow("Snake Game", img)

        # Check for hand interaction with buttons
        hands, img = detector.findHands(img, flipType=False)

        if hands:
            lmList = hands[0]['lmList']
            pointIndex = lmList[8][0:2]  # Get the fingertip position

            # Check if the hand points to any button
            if is_point_in_rect(pointIndex, start_button):
                return "start"
            elif is_point_in_rect(pointIndex, exit_button):
                cv2.destroyAllWindows()
                exit()

        # Wait for key press or hand interaction
        key = cv2.waitKey(1)
        if key == ord('s') or key == ord('S'):  # Start Game on pressing 'S'
            return "start"
        elif key == ord('q') or key == ord('Q'):  # Exit game on pressing 'Q'
            cv2.destroyAllWindows()
            exit()


def is_point_in_rect(point, rect):
    x, y = point
    x1, y1, x2, y2 = rect
    return x1 <= x <= x2 and y1 <= y <= y2


# Initialize the game class with a food image
game = SnakeGameClass("Donut.png")

while True:
    # Show the main menu
    menu_action = main_menu()

    if menu_action == "start":
        while True:
            success, img = cap.read()
            if not success:
                print("Error: Unable to read from camera")
                break  # Exit the loop if the camera fails to provide a frame

            img = cv2.flip(img, 1)  # Flip the image horizontally for mirror view
            hands, img = detector.findHands(img, flipType=False)

            if hands:
                lmList = hands[0]['lmList']
                pointIndex = lmList[8][0:2]
                img = game.update(img, pointIndex)

            # Display the image with the game and hand tracking
            cv2.imshow("Snake Game", img)

            key = cv2.waitKey(1)

            if key == ord('r') or key == ord('R'):  # Restart game on pressing 'R'
                game.gameOver = False
                game.score = 0  # Reset score
                game.points = []  # Clear the snake's points
                game.lengths = []  # Clear the snake's length history
                game.currentLength = 0  # Reset snake's length
                game.allowedLength = 150  # Reset allowed length
                game.previousHead = 0, 0  # Reset previous head position
                game.randomFoodLocation()  # Generate new food

            elif key == ord('m') or key == ord('M'):  # Return to main menu on pressing 'M'
                cv2.destroyWindow("Snake Game")  # Close the game window
                break  # Exit the current game and return to the main menu

cap.release()  # Release the camera after the loop
cv2.destroyAllWindows()  # Close all OpenCV windows
