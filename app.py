from flask import Flask, request, jsonify
import librosa
import numpy as np
import os
import soundfile as sf
import uuid

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['file']

    # 고유 파일명 생성
    temp_filename = f"{uuid.uuid4()}.webm"
    file.save(temp_filename)

    # webm → wav 변환
    wav_filename = temp_filename.replace('.webm', '.wav')
    try:
        data, samplerate = sf.read(temp_filename)
        sf.write(wav_filename, data, samplerate)
    except:
        return jsonify({'result': '오류: 변환 실패'}), 400

    # 음성 분석
    try:
        y, sr = librosa.load(wav_filename, sr=None)
        pitch = librosa.yin(y, fmin=50, fmax=300)
        energy = np.mean(np.abs(y))

        result = "truth"
        if np.std(pitch) > 30 or energy > 0.2:
            result = "lie"
    except Exception as e:
        return jsonify({'result': f'오류: {str(e)}'}), 500
    finally:
        os.remove(temp_filename)
        os.remove(wav_filename)

    return jsonify({'result': result})
