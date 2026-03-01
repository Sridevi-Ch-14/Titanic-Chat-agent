# Deployment Guide - Complete Step-by-Step

## Step 1: Initialize Git Repository

```bash
cd "c:\Users\Surya\Documents\Sridevi\Projects\Titanic project-internshala"

# Initialize git
git init

# Check status (should show .env is ignored)
git status

# Add all files
git add .

# Commit
git commit -m "Initial commit: Titanic chat agent"
```

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `titanic-chat-agent`
3. Keep it Public or Private
4. **DO NOT** initialize with README (you already have one)
5. Click "Create repository"

## Step 3: Push to GitHub

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/titanic-chat-agent.git

# Push code
git branch -M main
git push -u origin main
```

**Verify:** Your `.env` file should NOT appear on GitHub (protected by `.gitignore`)

## Step 4: Deploy Backend (FastAPI) - Using Render

### Option A: Render (Free Tier Available)

1. Go to https://render.com and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name:** `titanic-api`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn api:app --host 0.0.0.0 --port $PORT`
5. Click "Advanced" → "Add Environment Variable":
   - **Key:** `OPENAI_API_KEY`
   - **Value:** Your actual OpenAI API key
6. Click "Create Web Service"
7. Wait for deployment (5-10 minutes)
8. Copy your API URL (e.g., `https://titanic-api.onrender.com`)

### Option B: Railway (Alternative)

1. Go to https://railway.app and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Click "Add variables":
   - **Key:** `OPENAI_API_KEY`
   - **Value:** Your API key
5. Railway auto-detects Python and deploys
6. Copy your deployment URL

## Step 5: Update Frontend for Production

Before deploying frontend, update the API URL:

```bash
# Edit app.py and change line 4:
API_URL = "https://titanic-api.onrender.com"  # Your backend URL from Step 4
```

Commit and push:
```bash
git add app.py
git commit -m "Update API URL for production"
git push
```

## Step 6: Deploy Frontend (Streamlit) - Using Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select:
   - **Repository:** `YOUR_USERNAME/titanic-chat-agent`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click "Deploy"
6. Wait 2-3 minutes
7. Your app will be live at: `https://YOUR_USERNAME-titanic-chat-agent.streamlit.app`

## Alternative: Deploy Both on Same Platform

### Using Render for Both:

**Backend (already done in Step 4)**

**Frontend:**
1. Render Dashboard → "New +" → "Web Service"
2. Same repository
3. Configure:
   - **Name:** `titanic-frontend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
4. No environment variables needed (API_URL already set in code)
5. Deploy

## Verification Checklist

- [ ] Backend API is live and accessible
- [ ] Test backend: Visit `https://your-backend-url.com/` (should show status message)
- [ ] Test dataset endpoint: `https://your-backend-url.com/dataset-info`
- [ ] Frontend is live
- [ ] Frontend can connect to backend
- [ ] Test a query: "What percentage of passengers were male?"
- [ ] `.env` file is NOT on GitHub

## Troubleshooting

**Backend won't start:**
- Check logs on Render/Railway dashboard
- Verify `OPENAI_API_KEY` environment variable is set
- Ensure `requirements.txt` has all dependencies

**Frontend can't connect to backend:**
- Verify `API_URL` in `app.py` matches your backend URL
- Check CORS settings in `api.py` (should allow all origins with `*`)
- Test backend URL directly in browser

**OpenAI API errors:**
- Verify API key is valid
- Check OpenAI account has credits
- Check usage limits on OpenAI dashboard

## Cost Considerations

**Free Tiers:**
- **Render:** 750 hours/month free (sleeps after 15 min inactivity)
- **Railway:** $5 free credit/month
- **Streamlit Cloud:** Unlimited public apps
- **OpenAI:** Pay per use (GPT-3.5-turbo ~$0.002 per 1K tokens)

**Tip:** Use Render free tier for both services. Backend will sleep when inactive but wakes up on first request (takes ~30 seconds).

## Security Best Practices

1. **Use separate keys for dev/prod**
2. **Rotate keys regularly**
3. **Set usage limits on OpenAI dashboard**
4. **Monitor API usage**
5. **Never log API keys**
6. **Keep `.env` in `.gitignore`**
