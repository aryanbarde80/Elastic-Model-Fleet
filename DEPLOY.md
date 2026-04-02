# Deployment Guide — Elastic-Model-Fleet

Deploy any of the 100 models to Render.com with these steps.

---

## Step-by-Step Deployment

### Step 1: Push repo to GitHub
```bash
git clone https://github.com/aryanbarde80/Elastic-Model-Fleet.git
cd Elastic-Model-Fleet
git add .
git commit -m "Initial commit - 100 model fleet"
git push origin main
```

### Step 2: Go to render.com
Visit [https://render.com](https://render.com) and log in or sign up (free tier works).

### Step 3: Click "New +" → "Web Service"
From the Render dashboard, click the **New +** button in the top right, then select **Web Service**.

### Step 4: Connect GitHub repository
- Click **"Connect a repository"**
- Authorize Render to access your GitHub
- Select **Elastic-Model-Fleet**

### Step 5: Scroll to "Root Directory"
In the configuration page, find the **Root Directory** field and enter the folder path for the model you want to deploy:
```
weapons/sentiment-analysis-roberta
```
Replace `sentiment-analysis-roberta` with any folder name from `weapons/`.

### Step 6: Leave all other settings as default
- **Environment:** Docker (auto-detected)
- **Branch:** main
- **No environment variables needed**

### Step 7: Click "Deploy"
Scroll down and click the **Create Web Service** button.

### Step 8: Wait 2–10 minutes
Render will:
1. Pull your code
2. Build the Docker image
3. Download the HuggingFace model (this takes time — 500MB–2GB depending on model)
4. Start the FastAPI server

### Step 9: Use your API
Once deployed, your API is live at:
```
https://[service-name].onrender.com
```

Test it:
```bash
curl -X POST https://[service-name].onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is amazing!"}'
```

---

## Deploying Multiple Models

Each model needs its own Render Web Service. Repeat Steps 3–9 for each model, changing the Root Directory each time.

---

## Free Tier Notes

- Render free tier spins down after 15 minutes of inactivity (cold start ~30s)
- Models with large weights (>1GB) may need the **Starter** paid tier ($7/month)
- Recommended lightweight models for free tier: anything using `distilbert`, `minilm`, `tiny`, `small`, or `base` sized models

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Build fails | Check Root Directory is set correctly |
| Model load error | Check logs — model may need more RAM (upgrade tier) |
| Slow cold start | Normal on free tier — first request takes 30s |
| 500 error | Check `/health` endpoint — model may not have loaded yet |
