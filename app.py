from flask import Flask, render_template, Response
import cv2
import numpy as np
from keras.models import load_model

app = Flask(__name__,
            template_folder="template",
            static_folder="static")

# Load the fire detection model
model = load_model("fire_detection_model.h5")

def preprocess_image(img):
    img = cv2.resize(img, (128, 128))
    img = img / 255.0
    return img.reshape(-1, 128, 128, 3)

def detect_fire(frame):
    """Processes a frame and uses the ML model to predict fire."""
    processed_frame = preprocess_image(frame)
    prediction = model.predict(processed_frame)
    if prediction[0][1] > prediction[0][0]:
        return True
    else:
        return False

def generate_frames():
    """Generates frames from the webcam for video streaming."""
    cap = cv2.VideoCapture(0)
    try:
        if not cap.isOpened():
            print("Error: Could not open video stream.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if detect_fire(frame):
                cv2.putText(frame, "Fire Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    finally:
        cap.release()

@app.route('/')
def index():
    """Renders the home page."""
    return render_template('index.html')

@app.route('/fire_detection')
def fire_detection():
    """Renders the fire detection page."""
    return render_template('fire_detection.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/login')
def login():
    """Renders the login page."""
    return render_template('login.html')

@app.route('/feedback')
def feedback():
    """Renders the feedback page."""
    return render_template('feedback.html')

if __name__ == "__main__":
    app.run(debug=True)
