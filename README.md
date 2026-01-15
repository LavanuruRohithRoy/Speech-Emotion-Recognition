# 🎤 Speech Emotion Recognition (SER)

A clean, modular **Speech Emotion Recognition (SER)** system built using **Python, Machine Learning, and Flask**.
The project detects human emotions from speech audio, provides confidence scores, top predictions, and optional speech-to-text transcription.

---

## 🚀 What’s Different in This Version (Important)

This project is **not just a basic SER demo**. Compared to a naive MFCC + single-model setup, the following **practical improvements** were implemented:

* Calm emotion **merged with Neutral** to reduce real-world confusion
* Energy-based gating to avoid false *angry/fearful* predictions on low-energy speech
* Confidence thresholding with **"uncertain"** fallback
* Single, consistent feature-extraction pipeline (train = predict)
* Real microphone audio handling (not just dataset audio)

These changes focus on **stability, realism, and honest confidence**, not artificial accuracy inflation.

---

## 📊 Model Performance (Realistic)

| Metric   | Value                                                   |
| -------- | ------------------------------------------------------- |
| Accuracy | ~55–65%                                                 |
| F1 Score | ~55–60%                                                 |
| Classes  | Neutral, Happy, Sad, Angry, Fearful, Disgust, Surprised |

> Note: Speech Emotion Recognition is a difficult task.
> Acted datasets (RAVDESS) and real microphone audio differ significantly.

---

## 🧠 Machine Learning Approach

### Dataset

* **RAVDESS** (Ryerson Audio-Visual Database of Emotional Speech)
* Calm samples merged into Neutral

### Feature Extraction

Total features: ~190

* MFCC (mean, std, delta)
* Spectral centroid, bandwidth, rolloff
* Chroma features
* Spectral contrast
* Tonnetz
* Zero-crossing rate, RMS energy
* Harmonic & percussive components

All audio is:

* Mono
* 16 kHz sample rate

---

## 🤖 Model

* **RandomForestClassifier** (class-weight balanced)
* StandardScaler for normalization
* Confidence-based decision logic
* Uncertainty handling for low-confidence cases

---

## 🎯 Confidence Interpretation

| Confidence | Meaning               |
| ---------- | --------------------- |
| ≥ 70%      | High confidence       |
| 40–69%     | Medium confidence     |
| < 35%      | Marked as *uncertain* |

Low confidence does **not** mean failure — it means the model is being honest.

---

## 🌐 Application Features

* Upload audio file prediction
* Live microphone prediction
* Top-3 emotion probabilities
* Confidence color indicators
* Emoji-based emotion visualization
* Optional speech-to-text transcription

---

## 🏗️ Project Structure

```
SER/
│── app.py                 # Flask application
│── README.md
│── .gitignore
│
├── src/
│   ├── features/
│   │   └── audio_features.py   # Audio feature extraction
│   ├── models/
│   │   └── trainer.py          # Model training pipeline
│   ├── utils/
│   │   └── helpers.py          # Confidence & emoji helpers
│   ├── templates/              # HTML templates
│   └── static/                 # CSS, JS, assets
│
├── models/                     # Saved models (ignored in git)
├── temp/                       # Temporary audio files (ignored)
├── dataset/                    # Dataset (not included)
```

---

## ▶️ How to Run

### 1️⃣ Train the Model

```bash
python src/models/trainer.py
```

### 2️⃣ Run the Application

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

## ⚠️ Limitations

* Real-world accuracy depends heavily on audio quality
* Calm vs Neutral distinction is inherently ambiguous
* Transcription depends on external Google Speech API

---

## 📌 Use Cases

* Academic / learning projects
* Machine learning & signal processing demos
* Emotion-aware voice applications (research-level)

---

## 🔮 Future Improvements

See **IMPROVEMENTS.md** for:

* Deep learning models (CNN / LSTM / wav2vec)
* Database & API integration
* Deployment and scalability plans

---

## 📜 License

This project is intended for **educational and research purposes** only.
