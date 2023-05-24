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
