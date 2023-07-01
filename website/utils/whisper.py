import openai
import os
import io

class BytesIOWithFilename(io.BytesIO):
    def __init__(self, *args, name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

def convert_audio(audio_bytes, form_instance):
    """
    Converts audio file to text using OpenAI's Whisper ASR API.

    Args:
    - api_key (str): The API key for accessing the OpenAI API.
    - media_file_path (str): The path to the audio file.

    Returns:
    - None
    """

    #Get FormConfig settings
    form_template_instance = form_instance.template
    form_config_instance = form_template_instance.formconfig

    #language
    language = form_config_instance.language
    #conversation
    conversation_type = form_config_instance.conversation_type
    #audio_recognition_model
    audio_recognition_model_id = form_config_instance.audio_recognition_model_id

    with BytesIOWithFilename(audio_bytes, name=f'audio_file.webm') as media_file:
        response = openai.Audio.transcribe(
            api_key=os.environ.get('OPENAI_API_KEY'),
            model=audio_recognition_model_id,
            file=media_file,
            language=f"{language}",
            prompt=f"This is a conversation about {conversation_type} in {language}.",
            response_format='text'
        )
        return response