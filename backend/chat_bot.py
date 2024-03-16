from dotenv import load_dotenv
import google.generativeai as genai
import os
import re

#setup
load_dotenv()
api_key=os.getenv('api_key')
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

def gem_response(user_input):

    # Check if the user's input contains whole words related to pneumonia or healthcare
    pneumonia_keywords = ['pneumonia', 'lung infection', 'respiratory', 'breathing problem']
    healthcare_keywords = ['healthcare', 'medical', 'hospital', 'doctor', 'nurse']

    def contains_whole_word(input_str, keyword_list):
        return any(re.search(rf'\b{re.escape(keyword)}\b', input_str.lower()) for keyword in keyword_list)

    if contains_whole_word(user_input, pneumonia_keywords):
        # Process the request and get a response related to pneumonia
        convo = model.start_chat(history=[])
        convo.send_message(user_input)
        return convo.last.text
    elif contains_whole_word(user_input, healthcare_keywords):
        # Process the request and get a response related to healthcare
        convo = model.start_chat(history=[])
        convo.send_message(user_input)
        return convo.last.text
        print(user_input)
    else:
        # If the question is not related to pneumonia or healthcare, return a restricted response
        return "I'm sorry, I can only provide information related to pneumonia and healthcare."
