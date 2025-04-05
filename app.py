from flask import Flask, request, jsonify
import librosa
import numpy as np
import uuid
import os
import subprocess

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['file']
    webm_path = f"{uuid.uuid4()}.webm"
    wav_path = webm_path.replace('.webm', '.wav')

    file.save(webm_path)

    # ffmpeg로 webm → wav 변환
    try:
        subprocess.run(['ffmpeg', '-i', webm_path, wav_path], check=True)
    except subprocess.CalledProcessError:
        return jsonify({'result': '오류: ffmpeg 변환 실패'}), 500

    try:
        y, sr = librosa.load(wav_path, sr=None)
        pitch = librosa.yin(y, fmin=50, fmax=300)
        energy = np.mean(np.abs(y))

        result = "truth"
        if np.std(pitch) > 30 or energy > 0.2:
            result = "lie"
    except Exception as e:
        return jsonify({'result': f'분석 오류: {str(e)}'}), 500
    finally:
        os.remove(webm_path)
        os.remove(wav_path)

    return jsonify({'result': result})
