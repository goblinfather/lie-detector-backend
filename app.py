from flask import Flask, request, jsonify
import librosa
import numpy as np
import os

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['file']
    file.save('temp.wav')

    y, sr = librosa.load('temp.wav', sr=None)
    pitch = librosa.yin(y, fmin=50, fmax=300)
    energy = np.mean(np.abs(y))

    result = "truth"
    if np.std(pitch) > 30 or energy > 0.2:
        result = "lie"

    os.remove('temp.wav')
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
