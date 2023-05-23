import openai

def initialize_openai():
    API_KEY = input("API KEY: ")
    openai.api_key = API_KEY
    model_id = 'gpt-3.5-turbo'
    TEMPERATURE = 0.2
    return model_id, TEMPERATURE

def initialize_conversations():
    conversations = []
    conversations.append({'role': 'system', 'content': 
    """You are WhichDoctor AI, a medical assistant for a doctor processing inbound patients. Your goal is to help process the conversation and fill out the provided form queries.
    - The dialogue you are provided will consist of a conversation between a doctor and a patient. 
    - You will take this information provided and fill out the following form and write "N/A" if you do not have information to factually fill out any information.
    - The questions will be provided individually and you will answer one at a time.
    - You will only answer the question and not write anything else. If you need more information, write "N/A"."""
    })
    
    with open('testscript.txt', 'r') as file:
        testscript = file.read()
    
    conversations.append({'role': 'system', 'content': testscript})
    return conversations

def chatgpt_conversation(model_id, temperature, conversation_log):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation_log,
        temperature=temperature
    )
    
    conversation_log.append({
        'role': response.choices[0].message.role,
        'content': response.choices[0].message.content.strip()
    })
    
    tokens = response.usage['total_tokens']
    return tokens, conversation_log

