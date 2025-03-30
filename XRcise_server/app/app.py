from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import UserResponses
from app.model import predict_exercise
from fastapi.encoders import jsonable_encoder
import pandas as pd
import uvicorn
app = FastAPI()

# Add CORS middleware with more permissive settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.137.227:8080", "http://192.168.137.227:3000"],  # Add both frontend URLs
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    expose_headers=["*"]  # Exposes all headers
)

QUESTIONS = [
    {
        "id": 1,
        "question": "Where is your pain located?",
        "options": ["Shoulder Pain", "Back Pain", "Knee Pain", "Neck Pain", 
                    "Ankle Pain", "Elbow Pain", "PCOS Pain", "Osteoporotic (Weak Bones)"]
    },
    {
        "id": 2,
        "question": "What is your age group?",
        "options": ["Jan-18", "18-30", "30-50", "50+"]
    },
    {
        "id": 3,
        "question": "What is the intensity of your pain?",
        "options": ["Mild", "Moderate", "Intense"]
    },
    {
        "id": 4,
        "question": "What is your physical capacity?",
        "options": ["Easy", "Moderate", "Hard"]
    }
]

@app.get("/questions")
def get_questions():
    """Endpoint to get the list of questions."""
    return {"questions": QUESTIONS}

@app.post("/predict/")
async def predict(user_responses: UserResponses):
    """Endpoint to predict recommended exercise based on user input."""
    try:
        # Extract and transform the responses
        processed_data = user_responses.extract_responses()
        
        # Get predictions
        prediction_response = predict_exercise(processed_data)
        
        return jsonable_encoder(prediction_response)
    except Exception as e:
        return {"error": f"Prediction error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)