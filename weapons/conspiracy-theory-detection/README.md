# Conspiracy Theory Detection API

## What this model does
Identifies conspiracy theory language and framing in text.

**HuggingFace Model:** `facebook/bart-large-mnli`
**Task:** `zero-shot-classification`

## How to deploy on Render
1. Push this repository to GitHub
2. On [Render.com](https://render.com), click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Set **Root Directory** to: `weapons/conspiracy-theory-detection`
5. Click **"Deploy"**
6. Your API will be live at: `https://[service-name].onrender.com`

> **Note:** First deployment downloads the model (~100MB–1GB). Allow 3–10 minutes.

## API Endpoints

### POST /predict
Send text and get predictions.

**Request:**
```json
{
  "text": "your input text here",
  "parameters": {}
}
```

**Response:**
```json
{
  "result": "prediction output"
}
```

### POST /predict_batch
Send multiple texts at once.

**Request:**
```json
{
  "texts": ["text1", "text2", "text3"],
  "parameters": {}
}
```

**Response:**
```json
{
  "results": ["result1", "result2", "result3"]
}
```

### GET /health
Returns model health status.

### GET /info
Returns model metadata.

## Example Usage

**Python:**
```python
import requests

url = "https://your-service.onrender.com/predict"
response = requests.post(url, json={"text": "your text here"})
print(response.json())
```

**JavaScript:**
```javascript
fetch('https://your-service.onrender.com/predict', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({text: 'your text here'})
})
.then(res => res.json())
.then(console.log);
```

**cURL:**
```bash
curl -X POST https://your-service.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "your text here"}'
```

## Use Cases
- Content moderation
- Research tools
- Platform safety
- Fact-checking
- Media literacy education
