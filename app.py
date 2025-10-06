from flask import Flask, render_template, request
from fer import FER
import cv2
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
 
@app.route("/", methods=["GET", "POST"])
def index():
    mood = None
    filename = None

    if request.method == "POST":
        file = request.files["image"]
        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            # Read the image
            img = cv2.imread(file_path)

            # Detect emotions
            detector = FER(mtcnn=True)
            emotions = detector.detect_emotions(img)

            if emotions:
                top_emotion, score = detector.top_emotion(img)
                mood = f"{top_emotion.capitalize()} ({round(score * 100, 1)}%)"
            else:
                mood = "No face detected!"

            filename = file.filename

    return render_template("index.html", mood=mood, filename=filename)
