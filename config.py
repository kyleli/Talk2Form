import os

# GPT Config
MODEL_ID = 'gpt-3.5-turbo'
TEMPERATURE = 0.2
MAX_TOKENS = 4096
TRANSCRIPT_PATH = 'transcript.txt'

# Whisper Config
CONVERSATION_TYPE = "A Hospital Visit"
LANGUAGE = "English"
WHISPER_MODEL_ID = 'whisper-1'
AUDIO_PATH = 'output.wav'

# API Key
API_KEY = os.environ.get('OPENAI_API_KEY') # Change me to your OpenAI API key

# DEBUGGING
enable_audio_recording = True
enable_whisper = True
enable_gpt = True