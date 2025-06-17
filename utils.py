import cvzone
import cv2


# Function to draw a button and return the button area for collision checking
def draw_button(img, text, position, width, height):
    # Define button area as a tuple (x1, y1, x2, y2)
    button_rect = (position[0] - width // 2, position[1] - height // 2,
                   position[0] + width // 2, position[1] + height // 2)

    # Draw the text without the rectangle (border)
    cvzone.putTextRect(img, text, position, scale=2, thickness=2, offset=20)

    # Return the button's rectangular area for collision detection
    return button_rect


# Function to draw centered text
def draw_text(img, text, position, scale=1, thickness=1):
    cvzone.putTextRect(img, text, position, scale=scale, thickness=thickness, offset=20)
