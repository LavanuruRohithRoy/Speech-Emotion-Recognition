import os
import sys
import json
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from src.features.audio_features import AudioFeatureExtractor

MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

class SERModelTrainer:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.extractor = AudioFeatureExtractor(16000)
        self.scaler = StandardScaler()
        self.encoder = LabelEncoder()

    def _label_from_filename(self, name):
        code = int(name.split("-")[2])
        mapping = {
            1: "neutral",
            2: "neutral",   # calm MERGED
            3: "happy",
            4: "sad",
            5: "angry",
            6: "fearful",
            7: "disgust",
            8: "surprised"
        }
        return mapping.get(code)

    def load_data(self):
        X, y = [], []
        for actor in os.listdir(self.dataset_path):
            actor_dir = os.path.join(self.dataset_path, actor)
            if not os.path.isdir(actor_dir):
                continue
            for file in os.listdir(actor_dir):
                if file.endswith(".wav"):
                    path = os.path.join(actor_dir, file)
                    feat = self.extractor.extract(path)
                    label = self._label_from_filename(file)
                    if feat is not None and label:
                        X.append(feat)
                        y.append(label)
        return np.array(X), np.array(y)

    def train(self):
        print("Loading dataset...")
        X, y = self.load_data()

        y_enc = self.encoder.fit_transform(y)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_enc, test_size=0.2, stratify=y_enc, random_state=42
        )

        X_train = self.scaler.fit_transform(X_train)
        X_test = self.scaler.transform(X_test)

        model = RandomForestClassifier(
            n_estimators=300,
            class_weight="balanced",
            random_state=42
        )
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        metrics = {
            "accuracy": round(accuracy_score(y_test, y_pred) * 100, 2),
            "f1": round(f1_score(y_test, y_pred, average="weighted") * 100, 2),
            "precision": round(precision_score(y_test, y_pred, average="weighted") * 100, 2),
            "recall": round(recall_score(y_test, y_pred, average="weighted") * 100, 2),
            "classes": self.encoder.classes_.tolist(),
            "features": X.shape[1]
        }

        joblib.dump(model, os.path.join(MODELS_DIR, "model.pkl"))
        joblib.dump(self.scaler, os.path.join(MODELS_DIR, "scaler.pkl"))
        joblib.dump(self.encoder, os.path.join(MODELS_DIR, "label_encoder.pkl"))

        with open(os.path.join(MODELS_DIR, "model_metrics.json"), "w") as f:
            json.dump(metrics, f, indent=2)

        print("Training completed")
        print(metrics)

if __name__ == "__main__":
    DATASET_DIR = os.path.join(PROJECT_ROOT, "dataset")
    SERModelTrainer(DATASET_DIR).train()
