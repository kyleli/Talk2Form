import record
import whisper
import gpt
from config import *

def main():
    if ENABLE_AUDIO_RECORDING:
        record.record_audio(AUDIO_PATH)

    if ENABLE_WHISPER:
        if ENABLE_DEBUG_AUDIO:
            whisper.convert_audio(API_KEY, DEBUG_AUDIO_PATH)
        else:
            whisper.convert_audio(API_KEY, AUDIO_PATH)

    conversations = []
    if ENABLE_GPT:
        gpt.initialize_gpt(API_KEY)
        if ENABLE_DEBUG_TRANSCRIPT:
            conversations = gpt.initialize_system_prompt(SYSTEM_PROMPT, DEBUG_TRANSCRIPT_PATH)
        else:
            conversations = gpt.initialize_system_prompt(SYSTEM_PROMPT, TRANSCRIPT_PATH)
    if CUSTOM_QUERIES:
        gpt.process_user_input(conversations, MAX_TOKENS, MODEL_ID, TEMPERATURE)

if __name__ == '__main__':
    main()