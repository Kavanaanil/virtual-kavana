"""
Streamlit chatbot app - First-person personal assistant.
Uses RAG with FAISS and LLaMA via Groq API.
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from prompts import SYSTEM_PROMPT, REFUSAL_MESSAGE


# Page configuration
st.set_page_config(
    page_title="Personal Chatbot",
    page_icon="💬",
    layout="centered"
)


def ensure_vectorstore():
    """Build vector store if it doesn't exist (for Streamlit Cloud deployment)."""
    index_path = "vectorstore/faiss_index"
    if not os.path.exists(index_path) or not os.path.isdir(index_path):
        try:
            import ingest
            ingest.main()
        except Exception as e:
            st.error(f"Could not build knowledge base: {e}")
            st.stop()


@st.cache_resource
def load_vectorstore():
    """Load the FAISS vector store."""
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        try:
            # Try with the new parameter first (for newer versions)
            vectorstore = FAISS.load_local(
                "vectorstore/faiss_index",
                embeddings,
                allow_dangerous_deserialization=True
            )
        except TypeError:
            # Fall back to old parameter style for compatibility
            vectorstore = FAISS.load_local(
                "vectorstore/faiss_index",
                embeddings
            )
        return vectorstore
    except Exception as e:
        st.error(f"Failed to load vector store: {e}")
        st.info("Please run 'python ingest.py' first to create the vector store.")
        st.stop()


def format_docs(docs):
    """Format retrieved documents into a single string."""
    return "\n\n".join(doc.page_content for doc in docs)


@st.cache_resource
def setup_qa_chain(_vectorstore):
    """Setup the RetrievalQA chain with Groq (LLaMA API) using LCEL."""
    try:
        # Get API key from Streamlit secrets or environment
        try:
            api_key = st.secrets["GROQ_API_KEY"]
        except (KeyError, FileNotFoundError):
            api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            st.error("⚠️ GROQ_API_KEY not found!")
            st.info("Please set your Groq API key in Streamlit secrets or .env file")
            st.stop()
        
        # Initialize Groq with LLaMA
        llm = ChatGroq(
            groq_api_key=api_key,
            model_name="llama-3.3-70b-versatile",  # Latest LLaMA 3.3 model
            temperature=0.3,
        )
        
        # Create retriever
        retriever = _vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)
        
        # Create RAG chain using LCEL (LangChain Expression Language)
        qa_chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough()
            }
            | prompt
            | llm
            | StrOutputParser()
        )
        
        return qa_chain
        
    except Exception as e:
        st.error(f"Failed to setup QA chain: {e}")
        st.info("Make sure your GROQ_API_KEY is valid.")
        st.markdown("[Get a free Groq API key here](https://console.groq.com)")
        st.stop()


def initialize_session_state():
    """Initialize chat history in session state."""
    if "messages" not in st.session_state:
        st.session_state.messages = []


def display_chat_history():
    """Display all messages in the chat history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def main():
    """Main Streamlit app."""
    # Custom CSS for larger subtitle
    st.markdown("""
        <style>
        .big-subtitle {
            font-size: 24px;
            font-weight: 500;
            color: #555;
            margin-top: -10px;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header with image
    col1, col2 = st.columns([1, 4])
    with col1:
        # Display profile image (add your image to the root directory)
        try:
            st.image("profile.jpg", width=100)
        except:
            st.image("https://via.placeholder.com/100", width=100)
    with col2:
        st.title("Virtual Kavana")
        st.markdown('<p class="big-subtitle">Ask me anything about myself!</p>', unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    # Build vector store if missing (for Streamlit Cloud deployment)
    if not os.path.exists("vectorstore/faiss_index"):
        with st.spinner("Building knowledge base (first-time setup)..."):
            ensure_vectorstore()
    
    # Load resources
    with st.spinner("Loading knowledge base..."):
        vectorstore = load_vectorstore()
        qa_chain = setup_qa_chain(vectorstore)
    
    # Display chat history
    display_chat_history()
    
    # Chat input
    if prompt := st.chat_input("Ask me a question..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    answer = qa_chain.invoke(prompt)
                    
                    # Display response
                    st.markdown(answer)
                    
                    # Add to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })
                    
                except Exception as e:
                    error_msg = f"Error generating response: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
    
    # Sidebar with info
    with st.sidebar:
        st.header("About")
        st.info(
            "This chatbot answers questions about me based on my personal documents. "
            "All responses are grounded in my resume, bio, and project descriptions."
        )
        
        st.header("How to Use")
        st.markdown("""
        1. Ask any question about me
        2. Get answers in real-time
        3. All responses are fact-based
        """)
        
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()


if __name__ == "__main__":
    main()
