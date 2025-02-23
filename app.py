from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np

# Initialize FastAPI app
app = FastAPI()

# Load the trained model
MODEL_PATH = "decision_tree_model.pkl"  # Updated to use your model's path
try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    raise HTTPException(status_code=500, detail="Model file not found. Ensure the model is in the correct path.")

# Request body model for prediction
class PredictRequest(BaseModel):
    features: list

# Health check route
@app.get("/")
def read_root():
    return {"status": "API is running"}

# Prediction route
@app.post("/predict")
def predict(request: PredictRequest):
    try:
        # Convert input to NumPy array
        features = np.array(request.features).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(features)
        return {"prediction": int(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
