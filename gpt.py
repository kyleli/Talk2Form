import openai
from config import TRANSCRIPT_PATH

def initialize_gpt(API_KEY):
    openai.api_key = API_KEY

def initialize_system_prompt():
    """
    Initializes the conversations list with system instructions and transcript content.

    Returns:
    - conversations (list): A list of conversation objects.
    Each object represents a role and content in the conversation.
    """
    conversations = []
    conversations.append({'role': 'system', 'content': 
    """You are WhichDoctor AI, a medical assistant for a doctor processing inbound patients. Your goal is to help process the conversation and fill out the provided form queries.
    - The dialogue you are provided will consist of a conversation between a doctor and a patient. 
    - You will take this information provided and fill out the following form and write "N/A" if you do not have information to factually fill out any information.
    - The questions will be provided individually and you will answer one at a time.
    - You will only answer the question and not write anything else. If you need more information, write "N/A"."""
    })
    
    with open(TRANSCRIPT_PATH, 'r') as file:
        transcript = file.read()
    
    conversations.append({'role': 'system', 'content': transcript})
    return conversations

def new_conversation(model_id, temperature, conversation_log):
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
