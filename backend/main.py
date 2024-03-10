from flask import Flask,jsonify
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import os
import pickle
import numpy as np

from blood_report_predict import prediction

#gemini
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

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
# Ensure 'uploads' directory exists
uploads_dir = os.path.join(app.instance_path, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)

#load models
predict_model = pickle.load(open('model_training\models\RandomForest__model.pkl', 'rb'))

@app.route('/')
def home():
    return jsonify({"message": "prediction"}), 200

@app.route('/predict',methods=['POST'])
def predict():
    features = [x for x in request.form.values()]
    if len(features)==11:
        features_cleaned = [int(x) if x.isdigit() else 0 for x in features[2:]]
        predicted=prediction(features_cleaned)
        return jsonify({'Label':predicted[0],'Confidence':round(predicted[1],2)})

    else:
        return jsonify({'message':'Bad response'}),400

if __name__ == '__main__':
    #app.run(debug=True)
    pass