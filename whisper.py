import openai
from config import conversation_type, language

def convert_audio(api_key):
    media_file_path = 'testaudio.m4a'
    model_id = 'whisper-1'

    with open(media_file_path, 'rb') as media_file:
        response = openai.Audio.transcribe(
            api_key=api_key,
            model=model_id,
            file=media_file,
            prompt=f"This is a conversation about {conversation_type} in {language}.",
            response_format='text'
        )
        print(response)
        
if __name__ == '__main__':
    api_key = input("API KEY: ")
    convert_audio(api_key)