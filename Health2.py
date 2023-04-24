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
conversations.append({'role': 'system', 'content': """Doctor: Good morning, what brings you here today?

Patient: Hi doctor, I've been having this persistent pain in my lower abdomen and I'm worried it might be something serious.

Doctor: I see. How long ago was the first time you experienced it?

Patient: It started about two weeks ago.

Doctor: And what happened after that? Did the pain get worse or stay the same?

Patient: It's been pretty constant, but it seems to get worse when I'm walking or exercising.

Doctor: I see. And how did it change over the past few days?

Patient: It hasn't really changed much. It's still there, and it's still bothering me.

Doctor: Have you taken any medication or treatment for it?

Patient: I've been taking some over-the-counter painkillers, but they don't seem to be helping much.

Doctor: Alright. Have you had any similar illness in the past?

Patient: No, this is the first time I've had this kind of pain.

Doctor: Okay. Do you smoke, do drugs, drink alcohol? Do you eat and sleep well? Have there been any changes to your bathroom habits?

Patient: I don't smoke or do drugs, but I do drink alcohol occasionally. My diet and sleep habits are pretty good, and I haven't noticed any changes in my bathroom habits.

Doctor: That's good to know. Do you suffer from hypertension, diabetes, asthma, thyroid disorders, cancer or any chronic condition?

Patient: No, I don't have any of those conditions.

Doctor: Are you on any medication currently?

Patient: No, I'm not taking any medication right now.

Doctor: Do you have any known allergies?

Patient: Yes, I'm allergic to penicillin.

Doctor: Alright, thank you for letting me know. Have you had any surgeries?

Patient: No, I haven't had any surgeries.

Doctor: Has anyone in your immediate family suffered from any diseases like heart disease, cancer, genetic disease, psychiatric disorders, diabetes etc.?

Patient: My grandfather had heart disease, but no one else in my family has had any serious health issues.

Doctor: Okay. Based on what you've told me, it sounds like you may need to see a gastroenterologist. They specialize in the digestive system and can help diagnose and treat conditions like the one you're experiencing. I'll refer you to one and they'll be in touch with you soon to set up an appointment.

Patient: Alright, thank you doctor. I appreciate your help."""})

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