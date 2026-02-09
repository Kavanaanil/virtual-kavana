"""
Data ingestion script for personal chatbot.
Loads documents, creates embeddings, and builds FAISS vector store.
"""

import os
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


def load_documents(data_dir: str = "data"):
    """Load all documents from the data directory."""
    documents = []
    data_path = Path(data_dir)
    
    if not data_path.exists():
        raise FileNotFoundError(f"Data directory '{data_dir}' not found!")
    
    print(f"Loading documents from {data_dir}...")
    
    # Load PDF files
    for pdf_file in data_path.glob("*.pdf"):
        print(f"  Loading PDF: {pdf_file.name}")
        loader = PyPDFLoader(str(pdf_file))
        documents.extend(loader.load())
    
    # Load text files
    for txt_file in data_path.glob("*.txt"):
        print(f"  Loading TXT: {txt_file.name}")
        loader = TextLoader(str(txt_file), encoding="utf-8")
        documents.extend(loader.load())
    
    print(f"Loaded {len(documents)} document(s)")
    return documents


def split_documents(documents, chunk_size: int = 500, chunk_overlap: int = 50):
    """Split documents into chunks for embedding."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")
    return chunks


def create_vectorstore(chunks, vectorstore_path: str = "vectorstore/faiss_index"):
    """Create and save FAISS vector store."""
    print("Creating embeddings with sentence-transformers...")
    
    # Use HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    print("Building FAISS index...")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    # Save the vector store
    os.makedirs(os.path.dirname(vectorstore_path), exist_ok=True)
    vectorstore.save_local(vectorstore_path)
    
    print(f"Vector store saved to {vectorstore_path}")
    return vectorstore


def main():
    """Main ingestion pipeline."""
    print("=" * 50)
    print("Personal Chatbot Data Ingestion")
    print("=" * 50)
    
    try:
        # Load documents
        documents = load_documents("data")
        
        if not documents:
            print("ERROR: No documents found in data/ directory!")
            print("Please add resume.pdf, bio.txt, or projects.txt")
            return
        
        # Split documents
        chunks = split_documents(documents)
        
        # Create vector store
        create_vectorstore(chunks)
        
        print("\n" + "=" * 50)
        print("SUCCESS! Vector store created.")
        print("You can now run: streamlit run app.py")
        print("=" * 50)
        
    except Exception as e:
        print(f"\nERROR during ingestion: {e}")
        raise


if __name__ == "__main__":
    main()
