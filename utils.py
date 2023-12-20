import os

upload_folder = 'uploads'

def save_audio_file(file, filename):
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    return file_path

def transcribe_audio(client, audio_path):

    audio_file = open(audio_path, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )
    return transcript

def chat_with_gpt(client, transcript):

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant with english conversation. I will pass to you a text and you will response me with another text to continue the conversation. If the passed text isn't english, so send: this language is not english, please send a correc input."},
            {"role": "user", "content": transcript},
        ]
    )
    return response.choices[0].message.content

def generate_audio_response(client, content):

    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=content
    )
    return response