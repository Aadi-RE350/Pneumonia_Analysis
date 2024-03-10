from flask import Flask,jsonify

from blood_report_predict import prediction
from chat_bot import gem_response

#gemini
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "prediction"}), 200

@app.route('/predict',methods=['POST'])
def predict():
    labels = ['age', 'wbc count', 'crp level', 'esr level', 'procalcitonin level']
    symptoms = ['cough', 'chills', 'productive cough', 'chest pain', 'fatigue', 'shortness of breadth']

    values = []
    # Extract values for labels
    for label in labels:
        value = request.form.get(label)
        if value is not None:
            values.append(value)

    # Extract values for symptoms
    for symptom in symptoms:
        value = request.form.get(symptom,0) # by default zero
        if value is not None:
            values.append(value)

    if len(values)==11:
        #features_cleaned = [int(x) if x.isdigit() else 0 for x in features[2:]]
        predicted=prediction(values)
        return jsonify({'Label':predicted[0],'Confidence':round(predicted[1],2)}),200

    else:
        return jsonify({'message':values}),400

@app.route('/gemini',methods=['POST'])
def gemini_bot():
    user_input = request.json['user_input']
    genai_response = gem_response(user_input)
    return jsonify({'genai_response': genai_response}),200



if __name__ == '__main__':
    app.run(debug=True)