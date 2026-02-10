# Push KavanaBot to Your GitHub (kavanaanil78@gmail.com)

## Step 1: Create a new repository on GitHub

1. Open: **https://github.com/new**
2. Sign in with the account that uses **kavanaanil78@gmail.com** (username is likely **Kavanaanil**).
3. Fill in:
   - **Repository name:** `virtual-kavana` (or `KavanaBot` / any name you like)
   - **Description:** (optional) "Virtual Kavana - first-person personal chatbot"
   - **Visibility:** Public
   - **Do NOT** check "Add a README" (you already have files)
4. Click **Create repository**.

## Step 2: Push your code from your computer

Open **PowerShell** in your project folder and run (replace `REPO_NAME` with the name you used in Step 1, e.g. `virtual-kavana`):

```powershell
cd C:\Users\kavanaa\Downloads\KavanaBot

git remote add origin https://github.com/Kavanaanil/REPO_NAME.git
git push -u origin main
```

**Example** (if repo name is `virtual-kavana`):
```powershell
git remote add origin https://github.com/Kavanaanil/virtual-kavana.git
git push -u origin main
```

## Step 3: Sign in to GitHub when asked

- If Git asks for credentials, use:
  - **Username:** Your GitHub username (e.g. Kavanaanil)
  - **Password:** A **Personal Access Token** (GitHub no longer accepts account password for push)
- To create a token: GitHub → Settings → Developer settings → Personal access tokens → Generate new token. Give it `repo` scope.

## Done

After `git push` succeeds, your code will be at:
**https://github.com/Kavanaanil/REPO_NAME**

Then you can deploy on Streamlit Cloud (see DEPLOYMENT.md).
