from log import get_log
import os

log = get_log('english_conversation_ai_api.log')
upload_folder = 'uploads'

def save_audio_file(file, filename):
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    log.info(f'Arquivo {filename} salvo')
    return file_path

def transcribe_audio(client, audio_path):

    log.info('Iniciando transcrição de áudio para texto')

    audio_file = open(audio_path, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )
    return transcript

def chat_with_gpt(client, transcript):

    log.info('Enviando resposta para ChatGPT')
    log.info(f'Transcrição: {transcript}')

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant with english conversation. I will pass to you a text and you will response me with another text to continue the conversation. If the passed text isn't english, so send: this language is not english, please send a correc input."},
            {"role": "user", "content": transcript},
        ]
    )
    log.info(response)
    log.info(f'Resposta obtida com sucesso')
    return response.choices[0].message.content

def generate_audio_response(client, content):

    log.info(f'Conteúdo da resposta: {content}')
    log.info(f'Iniciando transformação de texto da resposta do ChatGPT para áudio')

    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=content
    )
    return response