import librosa
import numpy as np
import warnings

warnings.filterwarnings("ignore")

class AudioFeatureExtractor:
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate

    def extract(self, file_path):
        try:
            y, sr = librosa.load(file_path, sr=self.sample_rate, mono=True)

            if len(y) < sr * 0.5:
                return None

            features = []

            features.append(self._mfcc(y, sr))
            features.append(self._spectral(y, sr))
            features.append(self._chroma(y, sr))
            features.append(self._contrast(y, sr))
            features.append(self._tonnetz(y, sr))
            features.append(self._basic(y, sr))
            features.append(self._harmonic(y, sr))  # rhythm REMOVED

            features = [np.ravel(f) for f in features]
            return np.hstack(features).astype(np.float32)

        except Exception as e:
            print("Feature extraction error:", e)
            return None

    def _mfcc(self, y, sr):
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
        delta = librosa.feature.delta(mfcc)
        return np.hstack([
            np.mean(mfcc, axis=1),
            np.std(mfcc, axis=1),
            np.mean(delta, axis=1)
        ])

    def _spectral(self, y, sr):
        c = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        b = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
        r = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        return np.array([
            np.mean(c), np.std(c),
            np.mean(b), np.std(b),
            np.mean(r), np.std(r)
        ])

    def _chroma(self, y, sr):
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        return np.hstack([np.mean(chroma, axis=1), np.std(chroma, axis=1)])

    def _contrast(self, y, sr):
        contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        return np.hstack([np.mean(contrast, axis=1), np.std(contrast, axis=1)])

    def _tonnetz(self, y, sr):
        tonnetz = librosa.feature.tonnetz(
            y=librosa.effects.harmonic(y), sr=sr
        )
        return np.hstack([np.mean(tonnetz, axis=1), np.std(tonnetz, axis=1)])

    def _basic(self, y, sr):
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        rms = librosa.feature.rms(y=y)[0]
        flat = librosa.feature.spectral_flatness(y=y)[0]
        return np.array([
            np.mean(zcr), np.std(zcr),
            np.mean(rms), np.std(rms),
            np.mean(flat), np.std(flat)
        ])

    def _harmonic(self, y, sr):
        h, p = librosa.effects.hpss(y)
        return np.array([np.mean(h), np.mean(p)])
