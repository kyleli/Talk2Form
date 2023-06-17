import openai
import os

def initialize_system_prompt(SYSTEM_PROMPT, TRANSCRIPT_PATH):
    """
    Initializes the conversations list with system instructions and transcript content.

    Args:
    - SYSTEM_PROMPT (str): The system prompt or instructions for the conversation.
    - TRANSCRIPT_PATH (str): The path to the transcript file containing conversation content.

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
    - MODEL_ID (str): The ID of the GPT model to be used.
    - TEMPERATURE (float): The temperature value for generating responses.
    - PRESENCE_PENALTY (float): The presence penalty value for generating responses.
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

def process_form_query(response, SYSTEM_PROMPT, TRANSCRIPT_PATH, MODEL_ID='gpt-3.5-turbo', TEMPERATURE=0.2, PRESENCE_PENALTY=-0.2):
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    initialize_system_prompt(SYSTEM_PROMPT, TRANSCRIPT_PATH)
    conversations = []
    conversations.append({'role': 'user', 'content': question})
    tokens, conversations = new_entry(MODEL_ID, TEMPERATURE, PRESENCE_PENALTY, conversations)
    return f"{question} {conversations[-1]['content'].strip()}\n"