import os

# Whisper Config
CONVERSATION_TYPE = "A Hospital Visit"
LANGUAGE = "English"
WHISPER_MODEL_ID = 'whisper-1'
AUDIO_PATH = 'output.mp3'

# GPT Config
MODEL_ID = 'gpt-3.5-turbo'
TEMPERATURE = 0.2
PRESENCE_PENALTY = -0.2
MAX_TOKENS = 4096
TRANSCRIPT_PATH = 'transcript.txt'
SYSTEM_PROMPT = """
    You are WhichDoctor AI, a medical assistant for a doctor processing inbound patients. Your goal is to help process the conversation and fill out the provided form queries.
    - The dialogue you are provided will consist of a conversation between a doctor and a patient. 
    - You will take this information provided and fill out the following form and write "N/A" if you do not have information to factually fill out any information.
    - The questions will be provided individually and you will answer one at a time.
    - You will only answer the question and not write anything else. If you need more information or can not give a factual answer, write "N/A".
    """

# Form Config
FORM_PATH = 'debug_examples/full_form_single_line.txt'

# API Key
API_KEY = os.environ.get('OPENAI_API_KEY') # Change me to your OpenAI API key

# DEBUGGING MODULES
ENABLE_AUDIO_RECORDING = True
ENABLE_WHISPER = True
ENABLE_GPT = True
CUSTOM_QUERIES = True

# DEBUGGING EXAMPLE FILES
ENABLE_DEBUG_TRANSCRIPT = False
DEBUG_TRANSCRIPT_PATH = 'debug_examples/sample_transcript_2.txt'
ENABLE_DEBUG_AUDIO = False
DEBUG_AUDIO_PATH = 'debug_examples/64kbps_sample.mp3'