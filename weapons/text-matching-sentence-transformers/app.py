from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from transformers import pipeline

app = FastAPI(
    title="Text Matching Sentence Transformers API",
    description="Computes semantic similarity between text pairs using paraphrase-optimized MiniLM.",
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
    model_name = "sentence-transformers/paraphrase-MiniLM-L6-v2"
    try:
        model = pipeline("feature-extraction", model=model_name)
        print(f"Model {model_name} loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None

@app.post("/predict")
async def predict(data: InputData):
    if model is None:
        return {"error": "Model not loaded"}
    try:
            import numpy as np
    result = model(data.text)
    if isinstance(result, list):
        result = {"embeddings": result[0] if isinstance(result[0], list) else result}
    return {"result": result}
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@app.post("/predict_batch")
async def predict_batch(data: BatchInput):
    if model is None:
        return {"error": "Model not loaded"}
    try:
            results = [{"embeddings": model(t)} for t in data.texts]
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": model is not None}

@app.get("/info")
async def info():
    return {
        "model_name": "sentence-transformers/paraphrase-MiniLM-L6-v2",
        "task": "feature-extraction",
        "framework": "transformers",
        "ready": model is not None
    }
