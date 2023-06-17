import openai
import os

def convert_audio(audio_file, conversation_type='A Hospital Visit', language='english', WHISPER_MODEL_ID='whisper-1'):
    """
    Converts audio file to text using OpenAI's Whisper ASR API.

    Args:
    - api_key (str): The API key for accessing the OpenAI API.
    - media_file_path (str): The path to the audio file.

    Returns:
    - None
    """

    with open(audio_file.audio_file.path, 'rb') as media_file:
        response = openai.Audio.transcribe(
            api_key=os.environ.get('OPENAI_API_KEY'),
            model=WHISPER_MODEL_ID,
            file=media_file,
            prompt=f"This is a conversation about {conversation_type} in {language}.",
            response_format='text'
        )
        audio_file.transcript = response
        audio_file.save()