from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
import pandas as pd
from typing import List, Optional

app = FastAPI()

# Paths to model and datasets
MODEL_PATH = "decision_tree_model.pkl"
TRAIN_DATA_PATH = "churn-bigml-80.csv"            # Dataset 1: Training data
TEST_DATA_PATH = "churn-bigml-20.csv"              # Dataset 2: Test data

# Load the trained Decision Tree model at startup
model = None
if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        print("Decision Tree model loaded successfully from", MODEL_PATH)
    except Exception as e:
        print(f"Error loading model: {e}")
else:
    print(f"Model file not found at {MODEL_PATH}. Please ensure it's in the 'models' directory.")

# Load datasets (assuming CSV format)
def load_dataset(file_path, has_labels=True):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset not found at {file_path}")
    df = pd.read_csv(file_path)
    if has_labels:
        X = df.drop(columns=["label"]).values  # Adjust 'label' to your column name
        y = df["label"].values
        return X, y
    else:
        return df.values, None

# Input schemas
class PredictionInput(BaseModel):
    data: List[float]  # Single data point for prediction

class RetrainInput(BaseModel):
    data: List[List[float]]  # Training data
    labels: List[int]       # Corresponding labels
    hyperparams: Optional[dict] = None  # Optional Decision Tree hyperparameters

# Prediction endpoint
@app.post("/predict")
async def predict(input: PredictionInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    try:
        prediction = model.predict([input.data])[0]
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

# Test endpoint using Dataset 2
@app.get("/test")
async def test():
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    try:
        X_test, _ = load_dataset(TEST_DATA_PATH, has_labels=False)
        predictions = model.predict(X_test).tolist()
        return {"predictions": predictions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test error: {str(e)}")

# Retrain endpoint using Dataset 1 or custom input
@app.post("/retrain")
async def retrain(input: RetrainInput = None):
    if input and (not input.data or not input.labels):
        raise HTTPException(status_code=400, detail="Data and labels are required")
    if input and len(input.data) != len(input.labels):
        raise HTTPException(status_code=400, detail="Data and labels must match in length")

    try:
        from sklearn.tree import DecisionTreeClassifier  # Use Decision Tree
        
        # Use provided input or default to Dataset 1
        if input:
            X_train, y_train = input.data, input.labels
            hyperparams = input.hyperparams or {}
        else:
            X_train, y_train = load_dataset(TRAIN_DATA_PATH, has_labels=True)
            hyperparams = {}

        # Train the Decision Tree model
        model_instance = DecisionTreeClassifier(**hyperparams)  # e.g., max_depth, min_samples_split
        model_instance.fit(X_train, y_train)

        # Save and update the model
        joblib.dump(model_instance, MODEL_PATH)
        global model
        model = model_instance

        return {"message": "Decision Tree model retrained successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retraining error: {str(e)}")

@app.get("/")
async def root():
    return {"message": "MLOps FastAPI service with Decision Tree model"}
