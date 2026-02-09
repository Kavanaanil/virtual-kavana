# Quick Start Guide

## 🚀 Setup in 5 Minutes

### 1. Get Your API Key (2 minutes)

1. Go to **https://console.groq.com**
2. Sign up (it's free!)
3. Click **"Create API Key"**
4. Copy the key (starts with `gsk_...`)

### 2. Add Your API Key (1 minute)

Open the `.env` file and replace `your_groq_api_key_here` with your actual key:

```bash
GROQ_API_KEY=gsk_your_actual_key_here
```

### 3. Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

### 4. Build Vector Store (1 minute)

```bash
python ingest.py
```

### 5. Run the App!

```bash
streamlit run app.py
```

Your chatbot will open at **http://localhost:8501**

## 🎯 Customize Your Chatbot

Edit these files with YOUR information:
- `data/resume.txt` - Your resume
- `data/bio.txt` - Your biography
- `data/projects.txt` - Your projects

Then rebuild:
```bash
python ingest.py
```

## 🌐 Deploy to Cloud (Free)

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for complete deployment guide.

**TL;DR:**
1. Push to GitHub
2. Deploy on Streamlit Cloud (free)
3. Add your API key in Streamlit secrets
4. Done! Your chatbot runs 24/7

## ❓ Need Help?

- **API key issues**: Check `.env` file has correct key
- **Import errors**: Run `pip install -r requirements.txt` again
- **Deployment help**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **General issues**: See [README.md](README.md)

---

**That's it!** Your first-person AI chatbot is ready in 5 minutes! 🎉
