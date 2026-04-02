from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from transformers import pipeline

app = FastAPI(
    title="Text Summarization T5 API",
    description="Abstractive text summarization using DistilBART trained on CNN/DailyMail.",
    version="1.0.0"
)

model = None

class InputData(BaseModel):
    text: str
    parameters: Optional[Dict[str, Any]] = {}

class BatchInput(BaseModel):
    texts: List[str]
    parameters: Optional[Dict[str, Any]] = {}

@app.on_event("startup")
async def load_model():
    global model
    model_name = "sshleifer/distilbart-cnn-6-6"
    try:
        model = pipeline("summarization", model=model_name)
        print(f"Model {model_name} loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None

@app.post("/predict")
async def predict(data: InputData):
    if model is None:
        return {"error": "Model not loaded"}
    try:
            result = model(data.text)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@app.post("/predict_batch")
async def predict_batch(data: BatchInput):
    if model is None:
        return {"error": "Model not loaded"}
    try:
            results = [model(t) for t in data.texts]
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": model is not None}

@app.get("/info")
async def info():
    return {
        "model_name": "sshleifer/distilbart-cnn-6-6",
        "task": "summarization",
        "framework": "transformers",
        "ready": model is not None
    }
