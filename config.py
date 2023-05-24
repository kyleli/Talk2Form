import os

# GPT Config
MODEL_ID = 'gpt-3.5-turbo'
TEMPERATURE = 0.2
MAX_TOKENS = 4096

# Whisper Config
conversation_type = "A Hospital Visit"
language = "English"

# API Key
api_key = os.environ.get('OPENAI_API_KEY') # Change me to your OpenAI API key