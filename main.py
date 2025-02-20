import cv2

# Parameters
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
PLATE_CASCADE = cv2.CascadeClassifier('/Users/prudhviraj/Downloads/indian_license_plate.xml')
MIN_AREA = 200
COLOR = (255, 0, 255)

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(3, FRAME_WIDTH)
cap.set(4, FRAME_HEIGHT)
cap.set(10, 150)

# Error Handling
assert cap.isOpened(), "camera could not be opened!"

# Counter for file naming
counter = 0

while True:
    # Capture frame-by-frame
    success, img = cap.read()
    # print(success ," " ,img)
    if not success:
        break

    # Convert to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect number plates
    number_plates = PLATE_CASCADE.detectMultiScale(img_gray, 1.3, 7)

    # Iterate through detected plates
    for (x, y, w, h) in number_plates:
        area = w * h
        if area > MIN_AREA:
            # Draw rectangle around the plate
            cv2.rectangle(img, (x, y), (x + w, y + h), COLOR, 2)
            # Add text label
            cv2.putText(img, "License Plate", (x, y - 5),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, COLOR, 2)
            # Show region of interest (ROI)
            img_roi = img[y:y + h, x:x + w]
            cv2.imshow("ROI", img_roi)

            # Save ROI on 's' key press
            if cv2.waitKey(1) & 0xFF == ord('s'):
                SAVED_PATH = f"/Users/prudhviraj/Documents/CSE443/img_{counter}.png"
                cv2.imwrite(SAVED_PATH, img_roi)
                cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, "SAVED", (150, 265), cv2.FONT_HERSHEY_COMPLEX_SMALL, 4, COLOR, 2)
                cv2.waitKey(500)
                print(f"ROI saved as ROI_{counter}.png")
                counter += 1

    # Display the resulting frame
    cv2.imshow("OUTPUT", img)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release capture and close windows
cap.release()
cv2.destroyAllWindows()
