import librosa
import numpy as np

def analyze_audio(filepath):
    # 5초까지만 로딩 (메모리 절약)
    y, sr = librosa.load(filepath, sr=None, duration=5.0)

    # 특징 추출
    energy = np.mean(np.abs(y))
    pitch = librosa.yin(y, fmin=50, fmax=300)
    pitch_std = np.std(pitch)
    zcr = np.mean(librosa.feature.zero_crossing_rate(y))

    # 간단한 판단 로직
    score = 0
    if energy > 0.15:
        score += 1
    if pitch_std > 20:
        score += 1
    if zcr > 0.1:
        score += 1

    confidence = int((score / 3) * 100)
    result = "lie" if confidence >= 60 else "truth"

    return {
        'result': result,
        'confidence': confidence,
        'energy': round(energy, 3),
        'pitch_variability': round(pitch_std, 2),
        'zcr': round(zcr, 3)
    }
