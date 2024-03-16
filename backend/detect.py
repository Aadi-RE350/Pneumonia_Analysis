from flask import jsonify,request
import os
from werkzeug.utils import secure_filename
import requests
from dotenv import load_dotenv

load_dotenv()
def query(model_url, api_key, filename):
    API_URL = model_url
    headers = {"Authorization": f"Bearer {api_key}"}
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

def image_detection(uploads_dir,uploaded_file):
    
        if uploaded_file:
            # Save the uploaded file to the 'uploads' directory
            filename = os.path.join(uploads_dir, secure_filename(uploaded_file.filename))
            uploaded_file.save(filename)

            # Perform the model inference
            image_model_url = os.getenv('image_model_url')
            image_api_key=os.getenv('image_api_key')
            output = query(image_model_url, image_api_key, filename)

            # Clean up the uploaded file
            os.remove(filename)

            return output
        return {"error": "No file uploaded"}