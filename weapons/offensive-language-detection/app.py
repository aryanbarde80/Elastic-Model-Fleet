from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from transformers import pipeline

app = FastAPI(
    title="Offensive Language Detection API",
    description="Detects offensive language in text using RoBERTa trained on Twitter data.",
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
    model_name = "cardiffnlp/twitter-roberta-base-offensive"
    try:
        model = pipeline("text-classification", model=model_name)
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
        "model_name": "cardiffnlp/twitter-roberta-base-offensive",
        "task": "text-classification",
        "framework": "transformers",
        "ready": model is not None
    }
