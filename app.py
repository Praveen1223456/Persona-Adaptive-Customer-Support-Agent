import os
import streamlit as st
# Import only the main pipeline function from main.py
from main import run_customer_support_pipeline
# Import the Knowledge Base class to read files on startup
from src.rag_pipeline import SupportKnowledgeBase
from pypdf import PdfReader

st.set_page_config(page_title="Persona Support Hub", layout="wide")
st.title("⚡ Enterprise Persona-Adaptive AI Support Agent")

# --- START OF DOCUMENT INGESTION BLOCK ---
@st.cache_resource
def seed_knowledge_base():
    """Reads help documents on startup and saves them into the vector database."""
    kb = SupportKnowledgeBase()
    
    # Only load files if the database drawer is completely empty
    if kb.collection.count() == 0:
        # 1. Read Markdown File
        if os.path.exists("data/api_troubleshooting.md"):
            with open("data/api_troubleshooting.md", "r", encoding="utf-8") as f:
                kb.add_article("api_troubleshooting.md", f.read())
            
        # 2. Read Text Files
        if os.path.exists("data/billing_policy.txt"):
            with open("data/billing_policy.txt", "r", encoding="utf-8") as f:
                kb.add_article("billing_policy.txt", f.read())
            
        if os.path.exists("data/cookie_guide.txt"):
            with open("data/cookie_guide.txt", "r", encoding="utf-8") as f:
                kb.add_article("cookie_guide.txt", f.read())
            
        # 3. Read PDF File using pypdf
        if os.path.exists("data/password_reset_guide.pdf"):
            reader = PdfReader("data/password_reset_guide.pdf")
            pdf_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    pdf_text += text + "\n"
            kb.add_article("password_reset_guide.pdf", pdf_text)
            
    return kb

# Run the data loader quietly in the background
try:
    seed_knowledge_base()
except Exception as e:
    st.error(f"Error compiling vector documentation files: {e}")
# --- END OF DOCUMENT INGESTION BLOCK ---


# Text box where the user types their question
user_query = st.text_input("Customer Support Input:")

if st.button("Process Query") and user_query:
    with st.spinner("Processing..."):
        # Run our human-written pipeline function
        result = run_customer_support_pipeline(user_query)
        
        # Create two neat side-by-side columns on the screen
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 System Diagnostics")
            st.metric(label="Identified Customer Persona", value=result["detected_persona"])
            
            # Show if it went to a human or was handled by AI
            if result["escalated"]:
                st.warning("⚠️ Status: Routed to Human Queue")
            else:
                st.success("✅ Status: Resolved by AI")
                
            # Show which documents were read
            if result["sources_used"]:
                st.info(f"📚 Read from files: {', '.join(result['sources_used'])}")
                
        with col2:
            st.subheader("💬 Chat Response")
            # Show the message to the customer
            st.write(result["reply_text"])
            
            # If it was escalated, show the neat JSON package for the human expert
            if result["escalated"]:
                st.subheader("📁 Structured Human Handoff Record")
                st.json(result["handoff_details"])