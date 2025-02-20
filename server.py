from flask import Flask, Response, request
import numpy as np
import cv2

FRAME_WIDTH = 640
FRAME_HEIGHT = 480
PLATE_CASCADE = cv2.CascadeClassifier('/Users/prudhviraj/Downloads/indian_license_plate.xml')
MIN_AREA = 200
COLOR = (255, 0, 255)


from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
cap = cv2.VideoCapture(0)
counter = 0  # Counter for image filenames
imfile =[]
def generate_frames():
    
    while True:
        # read the camera frame
        success, frame = cap.read()
        
        if not success:
            break
        else:
            img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            number_plates = PLATE_CASCADE.detectMultiScale(img_gray, 1.3, 7)

            # Iterate through detected plates
            for (x, y, w, h) in number_plates:
                area = w * h
                if area > MIN_AREA:
                    # Draw rectangle around the plate
                    cv2.rectangle(frame, (x, y), (x + w, y + h), COLOR, 2)
                    # Add text label
                    cv2.putText(frame, "License Plate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, COLOR, 2)
                    # Show region of interest (ROI)
                    img_roi = frame[y:y + h, x:x + w]
                    imfile= img_roi

                    # Save ROI on 's' key press
                    if cv2.waitKey(1) & 0xFF == ord('s'):
                        SAVED_PATH = f"/Users/prudhviraj/Documents/CSE443/img/{counter}.png"
                        cv2.imwrite(SAVED_PATH, img_roi)
                        cv2.rectangle(frame, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
                        cv2.putText(frame, "SAVED", (150, 265), cv2.FONT_HERSHEY_COMPLEX_SMALL, 4, COLOR, 2)
                        cv2.waitKey(500)
                        print(f"ROI saved as ROI_{counter}.png")
                        counter += 1
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/save')
def save_image():
    global counter
    SAVED_PATH = f"/Users/prudhviraj/Documents/CSE443/img_{counter}.png"
    cv2.imwrite(SAVED_PATH, imfile)
    # cv2.rectangle(frame, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
    # cv2.putText(frame, "SAVED", (150, 265), cv2.FONT_HERSHEY_COMPLEX_SMALL, 4, COLOR, 2)
    # cv2.waitKey(500)
    print(f"ROI saved as ROI_{counter}.png")
    counter += 1
    return "Successfully"
    
    # print("Request data:", request.data)

    # if request.method == 'POST':
    #     try:
    #         # Convert raw binary data to numpy array
    #         nparr = np.frombuffer(request.data, np.uint8)
    #         img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    #         # Save the image with the provided filename
    #         SAVED_PATH = f"/Users/prudhviraj/Documents/CSE443/img_{counter}.png"
    #         cv2.imwrite(SAVED_PATH, img)
    #         counter += 1
    #         return 'Image saved successfully', 200
    #     except Exception global counteras e:
    #         print(f"Error saving image: {e}")
    #         return 'Internal server error', 500

if __name__ == "__main__":
    app.run(debug=True)
