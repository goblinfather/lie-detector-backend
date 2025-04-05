from flask import Flask, request, jsonify
from analyzer import analyze_audio
import os
import uuid

app = Flask(__name__)

# 업로드 최대 크기 제한 (2MB)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['file']
    filename = f"{uuid.uuid4()}.webm"
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
