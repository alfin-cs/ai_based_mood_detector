import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from deepface import DeepFace

# Flask setup
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"

# Allowed file types
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Emoji mapping for moods
EMOJI_MAP = {
    "happy": "😊",
    "sad": "😢",
    "angry": "😡",
    "surprise": "😲",
    "fear": "😨",
    "neutral": "😐",
    "disgust": "🤢"
}

@app.route("/", methods=["GET", "POST"])
def index():
    mood = None
    filename = None

    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        
        file = request.files["file"]

        if file.filename == "":
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            try:
                # Analyze mood using DeepFace
                result = DeepFace.analyze(img_path=file_path, actions=["emotion"], enforce_detection=False)
                mood = result[0]["dominant_emotion"].capitalize()
                emoji = EMOJI_MAP.get(mood.lower(), "")
                mood = f"{emoji} {mood}"
            except Exception as e:
                mood = f"Error: {str(e)}"

    return render_template("index.html", mood=mood, filename=filename)

if __name__ == "__main__":
    os.makedirs("static/uploads", exist_ok=True)
    app.run(debug=True)
