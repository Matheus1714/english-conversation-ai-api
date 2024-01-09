from log import get_log
import os

upload_folder = 'uploads'

log = get_log('speaking_ai.log')

def save_audio_file(file, filename):
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    log.info(f'Arquivo {filename} salvo')
    return file_path

def transcribe_audio(client, audio_path):

    log.info('Iniciando transcrição de áudio para texto')

    audio_file = open(audio_path, 'rb')
    transcript = client.audio.transcriptions.create(
        model='whisper-1',
        file=audio_file,
        response_format='text'
    )
    return transcript

def chat_with_gpt(client, content, **params):

    log.info('Enviando resposta para ChatGPT')
    log.info(f'Transcrição: {content}')

    language, model, temperature, *_ = params.values()

    prompt = f'You are an {language} conversation teacher. If I make a mistake in my speech, correct me. Speak to me only in {language}.'
    translated_content = translate_content(client, content, **params)

    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': translated_content},
        ]
    )

    log.info(response)
    log.info(f'Resposta obtida com sucesso')
    return response.choices[0].message.content

def translate_content(client, content, **params):

    language, model, *_ = params.values()
    prompt = f'Translate to {language} all my texts and send only the translation'

    response = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': content}
        ]
    )

    return response.choices[0].message.content

def generate_audio_response(client, content, **params):

    log.info(f'Conteúdo da resposta: {content}')
    log.info(f'Iniciando transformação de texto da resposta do ChatGPT para áudio')

    voice = params.get('voice', 'alloy')

    response = client.audio.speech.create(
        model='tts-1',
        voice=voice,
        input=content
    )
    return response