import record
import whisper
import gpt
from config import MODEL_ID, TEMPERATURE, MAX_TOKENS, API_KEY, AUDIO_PATH, enable_audio_recording, enable_gpt, enable_whisper

def main():
    if enable_audio_recording:
        record.record_audio(AUDIO_PATH)
    if enable_whisper:
        whisper.convert_audio(API_KEY, AUDIO_PATH)
    if enable_gpt:
        gpt.initialize_gpt(API_KEY)
        conversations = gpt.initialize_system_prompt()

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