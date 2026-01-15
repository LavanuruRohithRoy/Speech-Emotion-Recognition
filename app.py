from flask import Flask, render_template, request, send_from_directory
import os
import sys
import json
import joblib
import numpy as np
from werkzeug.utils import secure_filename
from pydub import AudioSegment
import librosa
import speech_recognition as sr

# -------------------------
# Path setup
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "src"))

from src.features.audio_features import AudioFeatureExtractor
from src.utils.helpers import get_confidence_color, get_emotion_emoji

# -------------------------
# Directories
# -------------------------
MODELS_DIR = os.path.join(BASE_DIR, "models")
TEMP_DIR = os.path.join(BASE_DIR, "temp")
STATIC_RECORDINGS_DIR = os.path.join("src", "static", "recordings")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(STATIC_RECORDINGS_DIR, exist_ok=True)

# -------------------------
# Load model artifacts
# -------------------------
model = joblib.load(os.path.join(MODELS_DIR, "model.pkl"))
scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.pkl"))
encoder = joblib.load(os.path.join(MODELS_DIR, "label_encoder.pkl"))

with open(os.path.join(MODELS_DIR, "model_metrics.json")) as f:
    model_metrics = json.load(f)

# -------------------------
# Objects
# -------------------------
extractor = AudioFeatureExtractor(sample_rate=16000)
recognizer = sr.Recognizer()

# -------------------------
# Flask app
# -------------------------
app = Flask(
    __name__,
    template_folder="src/templates",
    static_folder="src/static"
)

# -------------------------
# Utilities
# -------------------------
def transcribe_audio(wav_path):
    try:
        with sr.AudioFile(wav_path) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)
        print("TRANSCRIPT:", text)
        return text

    except sr.UnknownValueError:
        print("Transcript: Speech not clear")
        return "Speech not clear enough to transcribe"

    except sr.RequestError as e:
        print("Transcript API error:", e)
        return "Speech service unavailable"

    except Exception as e:
        print("Transcript error:", e)
        return "Transcript not available"


def predict_emotion(wav_path):
    # Energy gating
    y, _ = librosa.load(wav_path, sr=16000)
    rms = np.mean(librosa.feature.rms(y=y))

    if rms < 0.01:
        return "neutral", 40.0, []

    features = extractor.extract(wav_path)
    features = scaler.transform(features.reshape(1, -1))

    proba = model.predict_proba(features)[0]
    idx = np.argmax(proba)

    confidence = proba[idx] * 100
    emotion = encoder.inverse_transform([idx])[0]

    # Uncertainty handling
    if confidence < 35:
        emotion = "uncertain"

    top3 = np.argsort(proba)[::-1][:3]
    top_predictions = [
        {
            "emotion": encoder.inverse_transform([i])[0],
            "confidence": round(proba[i] * 100, 2),
            "emoji": get_emotion_emoji(
                encoder.inverse_transform([i])[0]
            )
        }
        for i in top3
    ]

    return emotion, round(confidence, 2), top_predictions

# -------------------------
# Routes
# -------------------------
@app.route("/")
def index():
    return render_template("index.html", model_metrics=model_metrics)

@app.route("/temp/<filename>")
def temp_file(filename):
    return send_from_directory(TEMP_DIR, filename)

# -------- Upload audio --------
@app.route("/predict", methods=["POST"])
def predict():
    file = request.files.get("audio")
    if not file:
        return "No file uploaded", 400

    filename = secure_filename(file.filename)
    raw_path = os.path.join(TEMP_DIR, filename)
    file.save(raw_path)

    wav_path = os.path.splitext(raw_path)[0] + ".wav"
    AudioSegment.from_file(raw_path).set_channels(1).set_frame_rate(
        16000
    ).export(wav_path, format="wav")

    emotion, confidence, top_predictions = predict_emotion(wav_path)
    transcript = transcribe_audio(wav_path)

    return render_template(
        "result.html",
        emotion=emotion,
        confidence=confidence,
        confidence_color=get_confidence_color(confidence),
        emotion_emoji=get_emotion_emoji(emotion),
        top_predictions=top_predictions,
        audio_file=f"/temp/{os.path.basename(wav_path)}",
        transcript=transcript,
        model_metrics=model_metrics
    )

# -------- LIVE MIC --------
@app.route("/predict_live", methods=["POST"])
def predict_live():
    file = request.files.get("audio")
    if not file:
        return "No audio received", 400

    webm_path = os.path.join(STATIC_RECORDINGS_DIR, "recorded_audio.webm")
    file.save(webm_path)

    wav_path = webm_path.replace(".webm", ".wav")
    AudioSegment.from_file(webm_path).set_channels(1).set_frame_rate(
        16000
    ).export(wav_path, format="wav")

    emotion, confidence, top_predictions = predict_emotion(wav_path)
    transcript = transcribe_audio(wav_path)

    return render_template(
        "result.html",
        emotion=emotion,
        confidence=confidence,
        confidence_color=get_confidence_color(confidence),
        emotion_emoji=get_emotion_emoji(emotion),
        top_predictions=top_predictions,
        audio_file=f"/static/recordings/{os.path.basename(wav_path)}",
        transcript=transcript,
        model_metrics=model_metrics
    )

# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
