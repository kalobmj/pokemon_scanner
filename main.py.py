import cv2
import os

# Connect to the S24 Ultra camera
camera = cv2.VideoCapture(1, cv2.CAP_MSMF)

# Create the images folder if it doesn't exist
os.makedirs("images", exist_ok=True)

# Start numbering saved images at 1
image_count = 1

# Check whether the camera opened successfully
if not camera.isOpened():
    print("Camera not opened")
else:
    print("Camera connected successfully!")
    print("Press S to save a picture")
    print("Press Q to quit")

    # Continuously display the camera feed
    while True:
        success, frame = camera.read()

        if not success:
            print("Failed to read frame")
            break

        # Display the live camera feed
        cv2.imshow("Pokemon Scanner", frame)

        # Check which key was pressed
        key = cv2.waitKey(1) & 0xFF

        # need to write logic to not override images in folder

        if key == ord('s'):
            # Create a filename for the image
            filename = f"images/card_{image_count}.jpg"

            # Save the current camera frame
            cv2.imwrite(filename, frame)

            print(f"Saved: {filename}")

            # Increase the number for the next image
            image_count += 1

        elif key == ord('q'):
            # Exit the camera loop
            break

# Release the camera and close all windows
camera.release()
cv2.destroyAllWindows()