# Text Simplification API

## What this model does
Simplifies complex text to make it more readable and accessible.

**HuggingFace Model:** `philippelaban/keep_it_simple`
**Task:** `text2text-generation`

## How to deploy on Render
1. Push this repository to GitHub
2. On [Render.com](https://render.com), click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Set **Root Directory** to: `weapons/text-simplification`
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
- Plain language conversion
- Accessibility tools
- Educational content
- Legal document simplification
- Medical information
