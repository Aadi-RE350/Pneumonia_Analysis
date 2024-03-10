import pickle
import numpy as np


#load models
predict_model = pickle.load(open('model_training\models\RandomForest__model.pkl', 'rb'))


def prediction(features_cleaned):
    #Age,White_Blood_Cell_Count,CRP_Level,Procalcitonin_Level,ESR_Level,Cough,Shortness of Breath,Chest Pain,Chills,Fatigue,Productive Cough
    final_features = [np.array(features_cleaned)]
    prediction = predict_model.predict_proba(final_features)
    confidence = dict(zip(predict_model.classes_, prediction[0] * 100))
    max_key = max(confidence, key=confidence.get)
    max_value = confidence[max_key]
    result = [max_key, max_value]

        # if max_key == 1:
        #     text = f'Pnuemonia Predicted with the confidence of {round(max_value, 2)}'

        # else:
        #     text = f'Pnuemonia Not found with the confidence of {round(max_value, 2)}'
        
    return result