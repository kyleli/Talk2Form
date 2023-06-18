import openai
import os

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
    
    return conversation_log

def process_form_query(form_response, audio_file):
    openai.api_key = os.environ.get('OPENAI_API_KEY')

    # Get Transcript
    TRANSCRIPT = audio_file.transcript

    # Get FormConfig
    form_template = form_response.form.template
    form_config = form_template.formconfig
    SYSTEM_PROMPT = form_config.system_prompt
    MODEL_ID = form_config.ai_model_id
    TEMPERATURE = float(form_config.temperature)
    PRESENCE_PENALTY = float(form_config.presence_penalty)

    # Get Question
    question = form_response.question.question

    conversations = []
    conversations.append({'role': 'system', 'content': SYSTEM_PROMPT})
    conversations.append({'role': 'system', 'content': TRANSCRIPT})
    conversations.append({'role': 'user', 'content': question})
    conversations = new_entry(MODEL_ID, TEMPERATURE, PRESENCE_PENALTY, conversations)
    form_response.response = conversations[-1]['content'].strip()
    form_response.save()