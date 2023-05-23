import gpt
import whisper

def main():
    model_id, temperature = gpt.initialize_openai()
    conversations = gpt.initialize_conversations()
    
    total_tokens = 0
    MAX_TOKENS = 4096
    
    while total_tokens <= MAX_TOKENS:
        try:
            prompt = input('Query: ')
        except KeyboardInterrupt:
            print("\nSYSTEM: You have force ended the conversation.")
            break
        
        conversations.append({'role': 'user', 'content': prompt})
        tokens, conversations = gpt.chatgpt_conversation(model_id, temperature, conversations)
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