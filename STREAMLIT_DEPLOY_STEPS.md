# Deploy Virtual Kavana on Streamlit Cloud – Do This Now

Your code is on GitHub. Follow these steps to go live.

---

## Step 1: Open Streamlit Cloud

If the deploy page didn’t open, go to: **https://share.streamlit.io**

Sign in with **GitHub** (same account as kavanaanil78@gmail.com).

---

## Step 2: Create a new app

1. Click **"New app"**.
2. Fill in:
   - **Repository:** `Kavanaanil/virtual-kavana`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL** (optional): e.g. `virtual-kavana` → your app will be at  
     `https://virtual-kavana.streamlit.app`

---

## Step 3: Add your Groq API key (required)

1. Click **"Advanced settings"**.
2. In the **Secrets** box, paste this and replace with your real key:

```toml
GROQ_API_KEY = "gsk_paste_your_actual_groq_key_here"
```

3. Get your key from: **https://console.groq.com/keys**  
   (Create one if you don’t have it.)

---

## Step 4: Deploy

1. Click **"Deploy"**.
2. Wait 3–8 minutes. Streamlit will install dependencies and build your app.
3. When it’s ready, you’ll see **"Your app is live!"** and a link like:  
   **https://virtual-kavana.streamlit.app**

---

## Step 5: Test your app

1. Open the app URL.
2. First load may take 10–30 seconds (building the knowledge base).
3. Ask something like: “What is your experience?” or “What are your skills?”

---

## Troubleshooting

- **"GROQ_API_KEY not found"**  
  In Streamlit Cloud: open your app → ⋮ → **Settings** → **Secrets** → add the line above and **Save**, then **Reboot app**.

- **App is slow to start**  
  Normal on first run. Later visits are faster.

- **Need a new Groq key**  
  https://console.groq.com → API Keys → Create API Key.

---

**After this, your Virtual Kavana chatbot will be live 24/7.**
