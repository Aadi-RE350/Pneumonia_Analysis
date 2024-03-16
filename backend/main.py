from flask import Flask,jsonify,request
from flask_cors import CORS
from blood_report_predict import prediction
from chat_bot import gem_response
from detect import image_detection
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "server runnung"}), 200

@app.route('/predict',methods=['POST'])
def predict():
    labels = ['age', 'wbcCount', 'crpLevel', 'esrLevel', 'procalcitoninLevel','cough', 'chills', 'productiveCough', 'chestPain', 'fatigue', 'shortnessOfBreath']
    values = []
    data=request.get_json()
    # Extract values for labels
    for label in labels:
        value = data.get(label)
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
    return jsonify({"User input":user_input,'genai_response': genai_response.replace('**', '').replace('\\n', '\n').replace('\\n*','\n')}),200

@app.route('/image_detect',methods=['POST'])
def image_detect():
    # Ensure 'uploads' directory exists
    uploads_dir = os.path.join(app.instance_path, 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    if request.method == 'POST':
        uploaded_file = request.files['image']
        if uploaded_file != None:
            return jsonify(image_detection(uploads_dir,uploaded_file)),200
        else:
            return jsonify({"message":"Make sure you select an image"})

if __name__ == '__main__':
    app.run(debug=True)