import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

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
                from deepface import DeepFace
                result = DeepFace.analyze(img_path=file_path, actions=["emotion"],enforce_detection=False,detector_backend="opencv")
                mood_raw = result[0]["dominant_emotion"].lower()
                emoji = EMOJI_MAP.get(mood_raw, "")
                mood = f"{emoji} {mood_raw.capitalize()}"
            except Exception as e:
                mood = f"Error: {str(e)}"

    return render_template("index.html", mood=mood, filename=filename)

if __name__ == "__main__":
    # When running locally with python app.py we allow specifying $PORT (Render provides $PORT in production)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
