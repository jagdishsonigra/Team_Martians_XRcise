import pickle
import numpy as np
import os
import pandas as pd

def get_model_paths():
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    MODEL_DIR = os.path.join(BASE_DIR, "models")
    return {
        "model": os.path.join(MODEL_DIR, "model.pkl"),
        "encoder": os.path.join(MODEL_DIR, "encoder.pkl"),
        "mapping": os.path.join(MODEL_DIR, "exercise_mapping.pkl"),
    }

def load_models():
    paths = get_model_paths()
    
    with open(paths["model"], "rb") as f:
        model = pickle.load(f)
    
    with open(paths["encoder"], "rb") as f:
        encoder = pickle.load(f)

    with open(paths["mapping"], "rb") as f:
        exercise_mapping = pickle.load(f)
    
    return model, encoder, exercise_mapping

def get_recommended_frequency(age_group, intensity, capacity):
    """Determine exercise frequency based on user characteristics"""
    if intensity == "Intense" or age_group == "50+":
        return "Weekly"
    elif capacity == "Easy":
        return "Daily"
    else:
        return "3-4 times per week"
  
def predict_exercise(user_responses):
    """Make a prediction using the trained model"""
    try:
        model, encoder, exercise_mapping = load_models()

        user_input_df = pd.DataFrame([[ 
            user_responses['responses']['pain_location'],  # Pain location
            user_responses['responses']['age_group'],      # Age group
            user_responses['responses']['pain_intensity'],  # Intensity
            user_responses['responses']['physical_capacity'] # Capacity
        ]], columns=["Painlocation", "Agegroup", "Intensity", "Capacity"])

        user_encoded = encoder.transform(user_input_df)

        prediction = int(model.predict(user_encoded)[0])

        recommended_exercise = exercise_mapping.get(prediction, "No exercise recommendation found")

        return {
            "prediction": prediction,
            "recommended_exercise": recommended_exercise,
            "frequency": get_recommended_frequency(
                user_responses['responses']['age_group'],
                user_responses['responses']['pain_intensity'],
                user_responses['responses']['physical_capacity']
            )
        }

    except Exception as e:
        return {"error": f"Prediction error: {str(e)}"}
