# Quick Start Guide

## Prerequisites Check

Before starting, ensure you have:

1. **Python 3.9+** installed
   ```bash
   python --version
   ```

2. **Ollama** installed and running
   ```bash
   # Download from: https://ollama.ai
   
   # Verify installation:
   ollama --version
   
   # Start Ollama:
   ollama serve
   ```

3. **LLaMA 3 model** downloaded
   ```bash
   ollama pull llama3
   ```

## Setup (First Time Only)

### Option 1: Automated Setup (Windows)
```bash
setup.bat
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Create vector store
python ingest.py
```

## Running the Chatbot

### Option 1: Quick Launch (Windows)
```bash
run.bat
```

### Option 2: Manual Launch
```bash
streamlit run app.py
```

The chatbot will open at: `http://localhost:8501`

## Using the Chatbot

### Example Questions You Can Ask:

**About Work Experience:**
- "What is your current role?"
- "Where have you worked?"
- "What companies did you work at?"
- "What is your experience with machine learning?"

**About Education:**
- "Where did you study?"
- "What degree do you have?"
- "Did you publish any papers?"

**About Projects:**
- "What projects have you built?"
- "Tell me about your AI projects"
- "What was your most impactful project?"

**About Skills:**
- "What programming languages do you know?"
- "What is your expertise?"
- "What technologies do you use?"

### Expected Behavior:

✅ **Good Responses (First Person):**
- "I worked at TechCorp as a Senior AI Engineer"
- "I hold a Master's degree from Stanford"
- "My expertise includes NLP and computer vision"

❌ **You will NOT see:**
- Third-person references ("Kavana worked at...")
- AI mentions ("As an AI assistant...")
- Hallucinations (making up information)

🚫 **Out-of-Scope Questions:**
If you ask something not in the documents:
- "I don't have that information in my profile yet."

## Customizing Your Chatbot

### Adding Your Own Documents

1. Replace files in `data/` folder:
   - `resume.txt` or `resume.pdf` - Your resume
   - `bio.txt` - Your biography
   - `projects.txt` - Your project descriptions

2. Rebuild the vector store:
   ```bash
   python ingest.py
   ```

3. Restart the chatbot:
   ```bash
   streamlit run app.py
   ```

### Supported Document Formats:
- PDF files (`.pdf`)
- Text files (`.txt`)

### Document Tips:
- Use clear headings and structure
- Include specific dates, numbers, and details
- Write in first or third person (the chatbot converts to first person)
- More detailed documents = better responses

## Troubleshooting

### Error: "Failed to load vector store"
**Solution:**
```bash
python ingest.py
```

### Error: "Make sure Ollama is running"
**Solution:**
```bash
# In a separate terminal:
ollama serve

# Then pull the model:
ollama pull llama3
```

### Error: "No documents found"
**Solution:**
- Add at least one document to `data/` folder
- Supported: `.pdf`, `.txt`

### Chatbot gives wrong information
**Solution:**
1. Check your source documents in `data/`
2. Rebuild vector store: `python ingest.py`
3. Restart chatbot

### Responses are too slow
**Solution:**
- Use a smaller model: `ollama pull llama3:7b`
- Reduce retrieved chunks in `app.py` (change `k=4` to `k=2`)

### Responses break character (third person)
**Solution:**
- The prompt in `prompts.py` is strict about first person
- If this happens, it may be hallucinating - check if information exists in documents
- Rebuild vector store: `python ingest.py`

## Advanced Configuration

### Change LLM Model
Edit `app.py`:
```python
llm = Ollama(
    model="mistral",  # or llama3.1, codellama, etc.
    temperature=0.3,
)
```

### Change Embedding Model
Edit `ingest.py` and `app.py`:
```python
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"  # or another model
)
```

### Adjust Response Creativity
Edit `app.py`:
```python
llm = Ollama(
    model="llama3",
    temperature=0.7,  # Higher = more creative (0.0 to 1.0)
)
```

### Change Chunk Settings
Edit `ingest.py`:
```python
chunks = split_documents(
    documents, 
    chunk_size=1000,  # Larger chunks = more context
    chunk_overlap=100  # More overlap = better continuity
)
```

## Tips for Best Results

1. **Detailed Documents**: More information = better answers
2. **Structured Content**: Use headings, bullet points, clear sections
3. **Specific Details**: Include dates, numbers, specific achievements
4. **Regular Updates**: Re-run `ingest.py` when you update documents
5. **Test Questions**: Try various phrasings to see what works best

## Clearing Chat History

Click the **"Clear Chat History"** button in the sidebar.

## Stopping the Chatbot

Press `Ctrl + C` in the terminal running Streamlit.

## Need Help?

Check the main README.md for more detailed documentation.
