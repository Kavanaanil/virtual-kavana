"""
Streamlit chatbot app - First-person personal assistant.
Uses RAG with FAISS and LLaMA via Groq API (for cloud deployment).
"""

import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from prompts import SYSTEM_PROMPT, REFUSAL_MESSAGE
import os


# Page configuration
st.set_page_config(
    page_title="Personal Chatbot",
    page_icon="💬",
    layout="centered"
)


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
            vectorstore = FAISS.load_local(
                "vectorstore/faiss_index",
                embeddings,
                allow_dangerous_deserialization=True
            )
        except TypeError:
            vectorstore = FAISS.load_local(
                "vectorstore/faiss_index",
                embeddings
            )
        return vectorstore
    except Exception as e:
        st.error(f"Failed to load vector store: {e}")
        st.info("Please run 'python ingest.py' first to create the vector store.")
        st.stop()


@st.cache_resource
def setup_qa_chain(_vectorstore):
    """Setup the RetrievalQA chain with Groq."""
    try:
        # Get API key from Streamlit secrets or environment
        groq_api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
        
        if not groq_api_key:
            st.error("GROQ_API_KEY not found!")
            st.info("Add your Groq API key to .streamlit/secrets.toml or set GROQ_API_KEY environment variable.")
            st.stop()
        
        # Initialize Groq with LLaMA
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.3,
            groq_api_key=groq_api_key,
        )
        
        # Create prompt template
        prompt_template = PromptTemplate(
            template=SYSTEM_PROMPT,
            input_variables=["context", "question"]
        )
        
        # Create retrieval chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=_vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            ),
            return_source_documents=False,
            chain_type_kwargs={"prompt": prompt_template}
        )
        
        return qa_chain
        
    except Exception as e:
        st.error(f"Failed to setup QA chain: {e}")
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
    # Header
    st.title("💬 Personal Chatbot")
    st.caption("Ask me anything about myself!")
    
    # Initialize session state
    initialize_session_state()
    
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
                    response = qa_chain.invoke({"query": prompt})
                    answer = response["result"]
                    
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
        
        st.divider()
        st.caption("Powered by LLaMA 3.1 via Groq & FAISS")


if __name__ == "__main__":
    main()
