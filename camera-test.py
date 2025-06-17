import cv2

# Try to open the default camera (index 0)
cap = cv2.VideoCapture(3)

if not cap.isOpened():  # Check if the camera is successfully opened
    print("Error: Camera not found or not accessible.")
else:
    print("Camera is accessible!")

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to capture image.")
            break

        # Display the camera feed
        cv2.imshow("Camera Feed", img)

        key = cv2.waitKey(1)
        if key == 27:  # Press ESC to exit
            break

    cap.release()
    cv2.destroyAllWindows()
