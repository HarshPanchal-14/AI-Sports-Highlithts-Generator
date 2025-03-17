import librosa
import numpy as np

class CrowdNoiseAnalyzer:
    def __init__(self, threshold=0.7):
        self.threshold = threshold
        
    def analyze_audio(self, audio_path):
        y, sr = librosa.load(audio_path)
        rms = librosa.feature.rms(y=y)
        mean_rms = np.mean(rms)
        return mean_rms > self.threshold 