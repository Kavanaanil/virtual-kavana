# Personal First-Person Chatbot

A Streamlit-based chatbot that answers questions about you using Retrieval-Augmented Generation (RAG), LLaMA 3, and FAISS vector store.

## Features

- **First-Person Responses**: The chatbot speaks only as "I", never in third person
- **RAG-Powered**: Uses FAISS vector store for semantic search over personal documents
- **Local LLM**: Runs LLaMA 3 locally via Ollama (no API keys needed)
- **Grounded Responses**: Only answers based on provided documents
- **Clean UI**: Professional Streamlit chat interface
- **Conversation History**: Maintains chat context throughout the session

## Prerequisites

1. **Python 3.9+**
2. **Groq API Key** (free) - Get it at https://console.groq.com

### Get Your Groq API Key

1. Go to **https://console.groq.com**
2. Sign up for a free account
3. Create an API key
4. Copy the key (starts with `gsk_...`)

## Installation

1. **Install dependencies**:

```bash
pip install -r requirements.txt
```

2. **Set up your API key**:

Create a `.env` file in the project root:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

Or for local development, you can also use `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

3. **Add your personal documents** to the `data/` folder:
   - `resume.pdf` or `resume.txt`
   - `bio.txt`
   - `projects.txt`
   - Any other personal documents

4. **Create the vector store**:

```bash
python ingest.py
```

This will:
- Load all documents from `data/`
- Split them into chunks
- Create embeddings using sentence-transformers
- Build and save FAISS index to `vectorstore/`

## Usage

**Run the Streamlit app**:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Project Structure

```
kavana_chatbot/
├── app.py              # Streamlit chat interface
├── ingest.py           # Data ingestion and FAISS creation
├── prompts.py          # System prompts for first-person behavior
├── requirements.txt    # Python dependencies
├── README.md           # This file
│
├── data/               # Personal documents
│   ├── resume.txt
│   ├── bio.txt
│   └── projects.txt
│
└── vectorstore/        # FAISS index (generated)
    └── faiss_index/
```

## How It Works

1. **Ingestion** (`ingest.py`):
   - Loads documents from `data/` (PDF and TXT)
   - Splits into chunks with overlap
   - Creates embeddings using `all-MiniLM-L6-v2`
   - Builds FAISS vector store

2. **Retrieval** (`app.py`):
   - User asks a question
   - System retrieves top-k relevant chunks from FAISS
   - Chunks are passed as context to LLaMA 3

3. **Generation** (`app.py`):
   - LLaMA 3 generates response using strict first-person prompt
   - Only uses information from retrieved context
   - Refuses to answer if information is missing

## Customization

### Modify System Prompt

Edit `prompts.py` to change the chatbot's behavior, tone, or rules.

### Change Chunk Size

Edit `ingest.py`:
```python
chunks = split_documents(documents, chunk_size=500, chunk_overlap=50)
```

### Change Number of Retrieved Chunks

Edit `app.py`:
```python
search_kwargs={"k": 4}  # Retrieve top 4 chunks
```

### Use Different LLM Model

Edit `app.py` (line ~47):
```python
llm = ChatGroq(
    groq_api_key=api_key,
    model_name="llama3-8b-8192",  # Smaller, faster model
    # Other options: "llama-3.1-70b-versatile", "mixtral-8x7b-32768"
    temperature=0.3,
)
```

## Troubleshooting

### "Failed to load vector store"
- Run `python ingest.py` first to create the FAISS index

### "GROQ_API_KEY not found"
- Make sure you've created `.env` file with your API key
- Or add it to `.streamlit/secrets.toml`
- Get API key at: https://console.groq.com

### "No documents found"
- Add your documents to `data/` folder
- Supported formats: PDF, TXT

### Slow responses
- Reduce chunk retrieval: `search_kwargs={"k": 2}`
- Use smaller model: `ollama pull llama3:7b`

## 🚀 Deployment

Want to deploy this chatbot to the cloud so it runs 24/7?

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for complete instructions on deploying to Streamlit Cloud.

## License

MIT License - Feel free to modify and use for your own personal chatbot!
