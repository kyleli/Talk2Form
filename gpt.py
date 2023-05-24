import openai

def initialize_gpt(API_KEY):
    openai.api_key = API_KEY

def initialize_system_prompt(SYSTEM_PROMPT, TRANSCRIPT_PATH):
    """
    Initializes the conversations list with system instructions and transcript content.

    Returns:
    - conversations (list): A list of conversation objects.
    Each object represents a role and content in the conversation.
    """
    conversations = []
    conversations.append({'role': 'system', 'content': SYSTEM_PROMPT})
    
    with open(TRANSCRIPT_PATH, 'r') as file:
        transcript = file.read()
    
    conversations.append({'role': 'system', 'content': transcript})
    return conversations

def new_entry(MODEL_ID, TEMPERATURE, PRESENCE_PENALTY, conversation_log):
    """
    Performs conversation completion using OpenAI's Chat API.

    Args:
    - model_id (str): The ID of the GPT model to be used.
    - temperature (float): The temperature value for generating responses.
    - conversation_log (list): A list of conversation objects representing the conversation history.

    Returns:
    - tokens (int): The total number of tokens used in the API response.
    - conversation_log (list): The updated conversation log with the new response appended.
    """
    response = openai.ChatCompletion.create(
        model=MODEL_ID,
        temperature=TEMPERATURE,
        presence_penalty=PRESENCE_PENALTY,
        messages=conversation_log
    )
    
    conversation_log.append({
        'role': response.choices[0].message.role,
        'content': response.choices[0].message.content.strip()
    })
    
    tokens = response.usage['total_tokens']
    return tokens, conversation_log

def process_user_input(MODEL_ID, TEMPERATURE, PRESENCE_PENALTY, conversations, MAX_TOKENS):
    total_tokens = 0

    while total_tokens <= MAX_TOKENS:
        try:
            prompt = input('Query: ')
        except KeyboardInterrupt:
            print("\nSYSTEM: You have force ended the conversation.")
            break

        conversations.append({'role': 'user', 'content': prompt})
        tokens, conversations = new_entry(MODEL_ID, TEMPERATURE, PRESENCE_PENALTY, conversations)
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
    conversations = []
    api_key = input("API KEY: ")
    initialize_gpt(api_key)
    initialize_system_prompt("""You are WhichDoctor AI, a medical assistant for a doctor processing inbound patients. Your goal is to help process the conversation and fill out the provided form queries.
    - The dialogue you are provided will consist of a conversation between a doctor and a patient. 
    - You will take this information provided and fill out the following form and write "N/A" if you do not have information to factually fill out any information.
    - The questions will be provided individually and you will answer one at a time.
    - You will only answer the question and not write anything else. If you need more information or can not give a factual answer, write "N/A".""", 'debug_examples/sample_transcript_2')
    process_user_input(conversations, 4096, "gpt-3.5-turbo", 0.2)