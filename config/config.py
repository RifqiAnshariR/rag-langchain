import re
from pathlib import Path

class Config:
    BASE_DIR = Path(__file__).parent.parent
    # ARTIFACTS_DIR = BASE_DIR / "artifacts"
    CONFIG_DIR = BASE_DIR / "config"
    DATA_DIR = BASE_DIR / "data"
    STATIC_DIR = BASE_DIR / "static"

    DATASET_FILE = DATA_DIR / "policy_manual.pdf"
    CSS_FILE = STATIC_DIR / "css/style.css"
    PAGE_ICON = STATIC_DIR / "img/favicon.ico"

    QDRANT_COLLECTION_NAME = "customer_assistant_collection"
    QDRANT_URL = "http://localhost:6333"
    # EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    EMBED_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
    LLM_MODEL_NAME = "gemini-2.5-flash"
    LLM_TEMPERATURE = 0
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 200

    PATTERNS = [
        re.compile(r'FINANCIAL LEADERSHIP THROUGH PROFESSIONAL EXCELLENCE.*?- \d+ -', re.DOTALL),
        re.compile(r'_+'),
        re.compile(r'\n\s*\n+'),
        re.compile(r' {2,}'),
        re.compile(r'<br\s*/?>'),
        re.compile(r'[\u0000-\u001F\u007F-\u009F]'),
    ]

    SYSTEM_PROMPT = (
        "You are a professional assistant named *MD Assistant*. "
        "Your responsibility is to give information about MD Company. "
        "Provide a concise and accurate answer based on the given context without unecessary explanation. "
        "If you don't know the answer, say you don't know. "
        "Context: {context}"
    )

    RETRIEVER_SEARCH_TYPE = "similarity_score_threshold"
    RETRIEVER_SEARCH_KWARGS = {"score_threshold": 0.5}