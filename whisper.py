import openai
from config import CONVERSATION_TYPE, LANGUAGE, WHISPER_MODEL_ID

def convert_audio(api_key, media_file_path):
    with open(media_file_path, 'rb') as media_file:
        response = openai.Audio.transcribe(
            api_key=api_key,
            model=WHISPER_MODEL_ID,
            file=media_file,
            prompt=f"This is a conversation about {CONVERSATION_TYPE} in {LANGUAGE}.",
            response_format='text'
        )
        with open("transcript.txt", 'w') as transcript_file:
            transcript_file.write(response)
        
if __name__ == '__main__':
    api_key = input("API KEY: ")
    convert_audio(api_key)