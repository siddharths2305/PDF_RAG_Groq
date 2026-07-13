# 🚀 Deployment Guide

## Quick Start for GitHub + Streamlit Cloud

### Step 1: Prepare Your Local Repository

```bash
# Navigate to the pdf-chatbot folder
cd pdf-chatbot

# Initialize git
git init

# Add files
git add .

# Create initial commit
git commit -m "Add PDF Chatbot app"

# Rename branch to main
git branch -M main
```

### Step 2: Create GitHub Repository

1. Go to [GitHub](https://github.com/new)
2. Create a new repository (e.g., `pdf-chatbot`)
3. **Do NOT** initialize with README (we already have one)
4. Copy the repository URL

### Step 3: Push Code to GitHub

```bash
# Add remote
git remote add origin <your-repo-url>

# Push to GitHub
git push -u origin main
```

### Step 4: Deploy on Streamlit Cloud

1. Go to [Streamlit Cloud](https://share.streamlit.io)
2. Click **"New app"**
3. Select:
   - **Repository**: Your GitHub repo
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Click **"Deploy"**

⏳ Wait 2-3 minutes for deployment to complete.

### Step 5: Add Secrets (IMPORTANT!)

1. Once deployed, click the **⋯** menu (top right)
2. Select **"Settings"**
3. Scroll to **"Secrets"** section
4. Add your Groq API key:
   ```
   GROQ_API_KEY = "your_actual_groq_api_key"
   ```
5. Save and rerun the app

## Your App URL

Once deployed, you'll get a public URL like:
```
https://your-username-pdf-chatbot.streamlit.app/
```

Share this URL with anyone to use your app!

## Environment Variables

### Local Development
Create a `.env` file (git-ignored):
```
GROQ_API_KEY=your_api_key
```

Load it in your app using `python-dotenv`:
```python
from dotenv import load_dotenv
load_dotenv()
```

### Streamlit Cloud
Add secrets in the Settings → Secrets panel (no `.env` file needed)

## Troubleshooting

### "No module named 'streamlit'"
```bash
pip install -r requirements.txt
```

### "GROQ_API_KEY not set"
- Local: Add to `.env` file
- Streamlit Cloud: Add to Settings → Secrets

### PDF Processing Issues
- Ensure PDF is text-based (not scanned image)
- Check that PDF isn't encrypted
- Try a smaller PDF first

### Slow Performance
- Streamlit Cloud has free tier limits
- Consider using a paid plan for faster inference
- Use smaller embedding models if needed

## Updates & Maintenance

To update your app:

```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push origin main
```

Streamlit Cloud will automatically redeploy within seconds!

## Resources

- [Streamlit Docs](https://docs.streamlit.io)
- [Groq API Docs](https://console.groq.com/docs)
- [LangChain Docs](https://python.langchain.com)
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)
