import os
from pathlib import Path
from dotenv import load_dotenv

# Locates the root workspace folder cleanly
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=ROOT_DIR / ".env")

class Config:
    # FIX: Make sure this variable name is typed exactly right!
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # Target Production LLM Engine Endpoints
    TEXT_MODEL = "gemini-2.5-flash"
    EMBEDDING_MODEL = "gemini-embedding-2"
    
    # Vector DB Storage Configurations
    DATABASE_FOLDER = str(ROOT_DIR / "chroma_db")
    
    # Confirmed high-sensitivity triggers for immediate human handoff routing
    URGENT_KEYWORDS = ["billing", "refund", "hack", "stolen", "lawsuit", "legal", "charge"]