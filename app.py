from flask import Flask, request, jsonify, Response
import requests
import os

app = Flask(__name__)

# API credentials and endpoint (set your API key via environment variable)
API_KEY = "sk_9582d61464c82800c1db15b8d4d09032fee51c19438142d7"
VOICE_ID = "29vD33N1CtxCmqQRPOHJ"
API_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

# Create a persistent session and headers
session = requests.Session()
headers = {
    "xi-api-key": API_KEY,
    "Content-Type": "application/json"
}

@app.route('/tts', methods=['POST'])
def tts_endpoint():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': "Missing 'text' key in JSON body."}), 400

    text = data['text']
    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.7,
            "similarity_boost": 0.8
        }
    }
    with session.post(API_URL, headers=headers, json=payload, stream=True) as response:
        if response.status_code == 200:
            # Use a generator to stream the audio data to the client
            def generate():
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        yield chunk
            return Response(generate(), content_type="audio/mpeg")
        else:
            error_msg = f"Error {response.status_code}: {response.text}"
            print(error_msg)
            return jsonify({'error': error_msg}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
