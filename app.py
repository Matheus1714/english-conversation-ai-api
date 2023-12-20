import os

from dotenv import dotenv_values
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from openai import OpenAI

from log import get_log
from utils import *

config = dotenv_values(".dev.env")

app = Flask(__name__)
CORS(app)

log = get_log('english_conversation_ai_api.log')

@app.route('/upload', methods=['POST'])
def upload_audio():
    try:
        if 'audio' not in request.files:
            msg = 'Nenhum arquivo de áudio enviado'
            log.info(msg)
            return jsonify({'error': msg}), 400

        audio_file = request.files['audio']
        audio_path = save_audio_file(audio_file, 'input.wav')

        client = OpenAI(api_key=config.get('OPEN_API_KEY'))

        transcript = transcribe_audio(client, audio_path)
        content = chat_with_gpt(client, transcript)
        response = generate_audio_response(client, content)

        speech_path = os.path.join(upload_folder, 'output.wav')
        response.stream_to_file(speech_path)

        log.info(f'Arquivo criado com sucesso!')
        return send_file(speech_path, as_attachment=True)

    except Exception as e:
        log.exception(e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
