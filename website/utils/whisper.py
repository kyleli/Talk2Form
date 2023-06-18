import openai
import os

def convert_audio(audio_file):
    """
    Converts audio file to text using OpenAI's Whisper ASR API.

    Args:
    - api_key (str): The API key for accessing the OpenAI API.
    - media_file_path (str): The path to the audio file.

    Returns:
    - None
    """

    #Get FormConfig settings
    form_instance = audio_file.form
    form_template_instance = form_instance.template
    form_config_instance = form_template_instance.formconfig

    #language
    language = form_config_instance.language
    #conversation
    conversation_type = form_config_instance.conversation_type
    #audio_recognition_model
    audio_recognition_model_id = form_config_instance.audio_recognition_model_id

    with open(audio_file.audio_file.path, 'rb') as media_file:
        response = openai.Audio.transcribe(
            api_key=os.environ.get('OPENAI_API_KEY'),
            model=audio_recognition_model_id,
            file=media_file,
            prompt=f"This is a conversation about {conversation_type} in {language}.",
            response_format='text'
        )
        audio_file.transcript = response
        audio_file.save()