import cv2


# Function to check how many cameras are available
def get_camera_count():
    index = 0
    available_cameras = []

    while True:
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            available_cameras.append(index)
            cap.release()
        else:
            break
        index += 1

    return available_cameras


# Function to test a selected camera
def test_camera(camera_index):
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print(f"Error: Camera {camera_index} not found or not accessible.")
        return False

    print(f"Camera {camera_index} is accessible!")
    while True:
        success, img = cap.read()
        if not success:
            print(f"Failed to capture image from camera {camera_index}.")
            break

        # Display the camera feed
        cv2.imshow(f"Camera Feed - {camera_index}", img)

        key = cv2.waitKey(1)
        if key == 27:  # Press ESC to exit
            break

    cap.release()
    cv2.destroyAllWindows()
    return True


def main():
    while True:
        available_cameras = get_camera_count()

        if not available_cameras:
            print("No cameras found.")
            return

        print("Available cameras:")
        for i, cam in enumerate(available_cameras):
            print(f"{i + 1}. Camera {cam}")

        # Ask user to choose a camera
        try:
            choice = int(
                input("Select a camera number to test (1 - {}), or 0 to exit: ".format(len(available_cameras))))
            if choice == 0:
                print("Exiting...")
                break
            if 1 <= choice <= len(available_cameras):
                camera_index = available_cameras[choice - 1]
                if not test_camera(camera_index):
                    print(f"Camera {camera_index} is not accessible or not working.")
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


if __name__ == "__main__":
    main()
