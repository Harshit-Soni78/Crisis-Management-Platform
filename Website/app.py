from flask import Flask, render_template, Response
import cv2
import numpy as np
from keras.models import load_model

app = Flask(__name__, template_folder="template")

model = load_model("fire_detection_model.h5")

def preprocess_image(img):
    img = cv2.resize(img, (128, 128))
    img = img / 255.0
    return img.reshape(-1, 128, 128, 3)

def detect_fire(frame):
    processed_frame = preprocess_image(frame)
    prediction = model.predict(processed_frame)
    if prediction[0][1] > prediction[0][0]:
        return True
    else:
        return False

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if detect_fire(frame):
            cv2.putText(frame, "Fire Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
