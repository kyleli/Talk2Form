import openai

# PARAMETERS: OpenAI API calls
API_KEY = input("API KEY: ")
openai.api_key = API_KEY
model_id = 'gpt-3.5-turbo'
TEMPERATURE = 0.2

# PARAMETERS: Maximum conversation length based on total tokens
total_tokens = 0
MAX_TOKENS = 4096

# Calling the ChatGPT API
def chatgpt_conversation(conversation_log):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation_log,
        temperature=TEMPERATURE
    )
    # Appending the output to the list of conversations
    conversation_log.append({
        'role': response.choices[0].message.role,
        'content': response.choices[0].message.content.strip()
    })
    tokens = response.usage['total_tokens']
    return tokens, conversation_log

# Appending the system prompt to the list of conversations
conversations = []
conversations.append({'role': 'system', 'content': 
"""You are WhichDoctor AI, a medical assistant for a doctor processing inbound patients. Your goal is to help process the conversation and fill out the provided form queries.
- The dialogue you are provided will consist of a conversation between a doctor and a patient. 
- You will take this information provided and fill out the following form and write "N/A" if you do not have information to factually fill out any information.
- The questions will be provided individually and you will answer one at a time.
- You will only answer the question and not write anything else. If you need more information, write "N/A"."""
})

# Inital system prompt (change later)
with open('testscript.txt', 'r') as file:
    testscript = file.read()

conversations.append({'role': 'system', 'content': testscript})

# Main input loop
while total_tokens <= MAX_TOKENS:
    try:
        prompt = input('Query: ')
    except KeyboardInterrupt:
        print("\nSYSTEM: You have force ended the conversation.")
        break
    conversations.append({'role': 'user', 'content': prompt})
    tokens, conversations = chatgpt_conversation(conversations)
    total_tokens += tokens
    print() # This is to add a space in terminal, remove in production
    # Check if the number of tokens generated has passed the maximum conversation length
    if total_tokens <= MAX_TOKENS:
        # Print the latest output
        if prompt.strip().endswith(":"):
            print(f"{prompt} {conversations[-1]['content'].strip()}\n")
        else:
            print(f"{prompt}: {conversations[-1]['content'].strip()}\n")
    else:
        print("You have processed the maximum number of tokens.")