import gpt
import whisper
from config import MODEL_ID, TEMPERATURE, MAX_TOKENS, api_key

def main():
    gpt.initialize_gpt(api_key)
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