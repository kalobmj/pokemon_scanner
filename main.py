import cv2
import os

from test_ocr import scan_card

# Connect to the S24 Ultra camera
camera = cv2.VideoCapture(1, cv2.CAP_MSMF)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

print("Width:", camera.get(cv2.CAP_PROP_FRAME_WIDTH))
print("Height:", camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create the images folder if it doesn't exist
os.makedirs("images", exist_ok=True)

# Find the highest existing image number
image_count = 1

for filename in os.listdir("images"):
    if filename.startswith("card_") and filename.endswith(".jpg"):
        number = filename.replace("card_", "").replace(".jpg", "")

        if number.isdigit():
            image_count = max(image_count, int(number) + 1)

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
            saved = cv2.imwrite(filename, frame)

            if saved:
                print(f"Saved: {filename}")

                # Increase the number for next image
                image_count += 1

                # Scan the saved image
                print("Scanning Pokemon card...")
                scan_card(filename)

            else:
                print("Failed to save image.")

        elif key == ord('q'):
            # Exit the camera loop
            break

# Release the camera and close all windows
camera.release()
cv2.destroyAllWindows()
