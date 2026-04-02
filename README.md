# Elastic-Model-Fleet 🚀

**100 deployable AI models. One repo. Zero configuration.**

Each folder inside `weapons/` is a fully self-contained FastAPI service you can deploy on [Render.com](https://render.com) in minutes — no environment variables, no secrets, no build settings.

---

## 🗂️ Repository Structure

```
Elastic-Model-Fleet/
├── weapons/
│   ├── sentiment-analysis-roberta/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── app.py
│   │   └── README.md
│   ├── named-entity-recognition-bert/
│   │   └── ...
│   └── ... (100 folders total)
├── MODELS.md       ← Full model index
├── DEPLOY.md       ← Deployment guide
├── test_all.py     ← Test all endpoints
└── client.py       ← Python client
```

---

## ⚡ Quick Deploy (30 seconds)

1. Fork/clone this repo and push to your GitHub
2. Go to [render.com](https://render.com) → **New +** → **Web Service**
3. Connect your GitHub repo
4. Set **Root Directory** to any folder, e.g. `weapons/sentiment-analysis-roberta`
5. Click **Deploy**
6. Get your URL: `https://your-service.onrender.com`
7. Send POST requests to `/predict` — done!

---

## 🧠 Available Models (100 total)

| Category | Examples |
|----------|---------|
| **Sentiment & Emotion** | sentiment-analysis-roberta, emotion-recognition, multilingual-sentiment |
| **NER & Extraction** | named-entity-recognition-bert, keyword-extraction, medical-ner |
| **Classification** | spam-classification, toxic-comment-detection, hate-speech-detection |
| **Generation** | text-summarization-t5, grammar-correction, response-generation |
| **Embeddings** | text-embeddings-minilm, semantic-search, document-clustering |
| **Biomedical** | drug-name-recognition, symptom-extraction, biomedical-relation-extraction |
| **Financial** | financial-sentiment-analysis, earning-call-analysis, stock-movement-prediction |
| **Legal** | legal-document-analysis, contract-clause-extraction |
| **Dialogue** | conversation-summarization, multi-turn-dialogue, empathetic-response-generation |

See [MODELS.md](MODELS.md) for the full list with examples.

---

## 📡 API Shape (same for all 100 models)

```
POST /predict        → Single prediction
POST /predict_batch  → Batch predictions
GET  /health         → Health check
GET  /info           → Model metadata
```

---

## 🔑 No Auth Required

All APIs are open. No API keys. No environment variables. Deploy and call.
