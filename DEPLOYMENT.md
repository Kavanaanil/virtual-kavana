# Deploy Virtual Kavana on Streamlit Cloud (Always Running)

Follow these steps to deploy your chatbot so it runs 24/7 and is accessible from anywhere.

---

## Prerequisites

1. **GitHub account** – [github.com](https://github.com)
2. **Streamlit Cloud account** – [share.streamlit.io](https://share.streamlit.io) (free)
3. **Groq API key** – [console.groq.com](https://console.groq.com) (free)

---

## Step 1: Push Your Code to GitHub

### 1.1 Create a new repository on GitHub

1. Go to **https://github.com/new**
2. Repository name: e.g. `virtual-kavana` or `kavana-chatbot`
3. Visibility: **Public**
4. Do **not** add README, .gitignore, or license (you already have files)
5. Click **Create repository**

### 1.2 Push from your computer

Open **PowerShell** or **Command Prompt** in your project folder and run:

```powershell
cd C:\Users\kavanaa\Downloads\KavanaBot

git init
git add .
git commit -m "Virtual Kavana chatbot - ready for Streamlit Cloud"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your GitHub username and repo name.

**Note:** Your `.gitignore` already excludes `.env` and `.streamlit/secrets.toml`, so your API key will **not** be uploaded. You will add it securely in Streamlit Cloud in the next step.

---

## Step 2: Deploy on Streamlit Cloud

### 2.1 Open Streamlit Cloud

1. Go to **https://share.streamlit.io**
2. Sign in with your **GitHub** account
3. Click **"New app"**

### 2.2 Configure the app

1. **Repository:** `YOUR_USERNAME/YOUR_REPO_NAME`
2. **Branch:** `main`
3. **Main file path:** `app.py`
4. **App URL:** (optional) e.g. `virtual-kavana` → your app will be at  
   `https://virtual-kavana.streamlit.app`

### 2.3 Add your Groq API key (required)

1. Click **"Advanced settings"**
2. In **Secrets**, paste (replace with your real key):

```toml
GROQ_API_KEY = "gsk_your_actual_groq_api_key_here"
```

3. Get your key from: [console.groq.com → API Keys](https://console.groq.com/keys)

### 2.4 Deploy

1. Click **"Deploy"**
2. Wait 3–8 minutes. Streamlit will:
   - Clone your repo
   - Install dependencies from `requirements.txt`
   - Build the knowledge base from `data/` on first run
   - Start the app

3. When it’s ready, you’ll see: **"Your app is live!"** with a link like  
   `https://virtual-kavana.streamlit.app`

---

## Step 3: Keep It Running (Always On)

### Free tier (default)

- App **sleeps** after ~15 minutes of no visits.
- **Wakes up** when someone opens the link (may take 10–30 seconds).
- No extra setup; good for personal use.

### Option A: Keep it warm (free)

Use **UptimeRobot** to open your app every 5 minutes so it rarely sleeps:

1. Go to **https://uptimerobot.com** and create a free account.
2. Click **"+ Add New Monitor"**
3. **Monitor Type:** HTTP(s)
4. **Friendly Name:** Virtual Kavana
5. **URL:** `https://YOUR_APP_NAME.streamlit.app`
6. **Monitoring Interval:** 5 minutes
7. Click **"Create Monitor"**

Your app will be pinged every 5 minutes and stay warm most of the time.

### Option B: Always on (paid)

- In **Streamlit Cloud**, upgrade to a **Team** plan.
- Your app can then be set to **always on** (no sleep).

---

## Updating Your Deployed App

### Update text (bio, resume, projects)

1. Edit files in the `data/` folder (locally or on GitHub).
2. Commit and push:

```powershell
git add data/
git commit -m "Update personal info"
git push
```

3. In Streamlit Cloud, open your app → **"Manage app"** → **"Reboot app"**  
   (or wait for the next deploy; some plans auto-redeploy on push).

The next time the app runs, it will rebuild the knowledge base from the updated `data/` files.

### Update code (e.g. app.py, prompts.py)

1. Edit the files locally.
2. Commit and push:

```powershell
git add .
git commit -m "Describe your change"
git push
```

3. Streamlit Cloud will redeploy automatically (or use **"Reboot app"** if needed).

---

## Troubleshooting

### "GROQ_API_KEY not found"

- In Streamlit Cloud: **App → Settings (⋮) → Secrets**
- Add: `GROQ_API_KEY = "gsk_..."`  
- Save and **Reboot app**

### "Failed to load vector store"

- The app will try to build the knowledge base from `data/` on first run.
- Ensure `data/` contains at least one of: `bio.txt`, `projects.txt`, `resume.txt` (or `resume.pdf`).
- If it still fails, run `python ingest.py` locally, then add and push the `vectorstore/` folder (and remove `vectorstore/` from `.gitignore` for that repo if you want to commit it).

### App is slow to open

- Normal on free tier after sleep; first load can take 10–30 seconds.
- Use UptimeRobot (above) to reduce how often it sleeps.

### Need help

- Streamlit Cloud docs: [docs.streamlit.io/streamlit-community-cloud](https://docs.streamlit.io/streamlit-community-cloud)
- Groq: [console.groq.com/docs](https://console.groq.com/docs)

---

## Summary

| Step | Action |
|------|--------|
| 1 | Push project to GitHub (repo public) |
| 2 | In Streamlit Cloud: New app → connect repo, main file `app.py` |
| 3 | In Advanced settings → Secrets: add `GROQ_API_KEY` |
| 4 | Deploy and use the live URL |
| 5 | (Optional) Add UptimeRobot monitor to keep app warm |

After this, your **Virtual Kavana** chatbot will be live and usable 24/7 at your Streamlit Cloud URL.
