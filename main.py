import record
import whisper
import gpt
from config import MODEL_ID, TEMPERATURE, MAX_TOKENS, API_KEY, AUDIO_PATH, ENABLE_AUDIO_RECORDING, ENABLE_GPT, ENABLE_WHISPER, ENABLE_DEBUG_AUDIO, DEBUG_AUDIO_PATH, ENABLE_DEBUG_TRANSCRIPT, DEBUG_TRANSCRIPT_PATH, TRANSCRIPT_PATH, SYSTEM_PROMPT

def main():
    if ENABLE_AUDIO_RECORDING:
        record.record_audio(AUDIO_PATH)
    if ENABLE_WHISPER:
        if ENABLE_DEBUG_AUDIO:
            whisper.convert_audio(API_KEY, DEBUG_AUDIO_PATH)
        else:
            whisper.convert_audio(API_KEY, AUDIO_PATH)
    if ENABLE_GPT:
        gpt.initialize_gpt(API_KEY)
        if ENABLE_DEBUG_TRANSCRIPT:
            conversations = gpt.initialize_system_prompt(SYSTEM_PROMPT, DEBUG_TRANSCRIPT_PATH)
        else:
            conversations = gpt.initialize_system_prompt(SYSTEM_PROMPT, TRANSCRIPT_PATH)

    total_tokens = 0

    while total_tokens <= MAX_TOKENS:
        try:
            prompt = input('Query: ')
        except KeyboardInterrupt:
            print("\nSYSTEM: You have force ended the conversation.")
            break

        conversations.append({'role': 'user', 'content': prompt})
        tokens, conversations = gpt.new_conversation(MODEL_ID, TEMPERATURE, conversations)
        total_tokens += tokens
        print()

        if total_tokens <= MAX_TOKENS:
            if prompt.strip().endswith(":"):
                print(f"{prompt} {conversations[-1]['content'].strip()}\n")
            else:
                print(f"{prompt}: {conversations[-1]['content'].strip()}\n")
        else:
            print("You have processed the maximum number of tokens.")

if __name__ == '__main__':
    main()