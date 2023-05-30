import record
import whisper
import gpt
import formprocessing
from config import *

def main():
    if ENABLE_AUDIO_RECORDING:
        record.record_audio(AUDIO_PATH)
    else:
        print("Audio Recording Disabled")

    if ENABLE_WHISPER:
        if ENABLE_DEBUG_AUDIO:
            whisper.convert_audio(API_KEY, DEBUG_AUDIO_PATH)
        else:
            whisper.convert_audio(API_KEY, AUDIO_PATH)
    else:
        print("Whisper Disabled")

    conversations = []
    if ENABLE_GPT:
        gpt.initialize_gpt(API_KEY)
        if ENABLE_DEBUG_TRANSCRIPT:
            conversations = gpt.initialize_system_prompt(SYSTEM_PROMPT, DEBUG_TRANSCRIPT_PATH)
        else:
            conversations = gpt.initialize_system_prompt(SYSTEM_PROMPT, TRANSCRIPT_PATH)
    else:
        print("GPT Disabled")

    if CUSTOM_QUERIES:
        print("Using Custom Queries")
        gpt.process_user_input(MODEL_ID, TEMPERATURE, PRESENCE_PENALTY, conversations, MAX_TOKENS)
    else:
        print("Processing Questions")
        questions = formprocessing.read_questions_from_file(FORM_PATH)
        answers = []
        for question in questions:
            answer = gpt.process_form_query(MODEL_ID, TEMPERATURE, PRESENCE_PENALTY, conversations, question)
            answers.append(answer)
        formprocessing.write_answers_to_file(answers)
        print("Completed Processing")

if __name__ == '__main__':
    main()