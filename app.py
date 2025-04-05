from flask import Flask, request, jsonify
from analyzer import analyze_audio
import os
import uuid

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['file']
    filename = f"{uuid.uuid4()}.wav"
    file.save(filename)

    try:
        result = analyze_audio(filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(filename)

    return jsonify(result)

if __name__ == "__main__":
    app.run()
