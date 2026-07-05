import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    UPLOAD_DIR = "/tmp/uploads" if os.environ.get('VERCEL') else "uploads"
    DB_DIR = "/tmp/db" if os.environ.get('VERCEL') else "db"
    EMBEDDING_MODEL = "mistral-embed"
    LLM_MODEL = "mistral-small"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    RETRIEVER_K = 3
    RETRIEVER_FETCH_K = 10
    RETRIEVER_LAMBDA = 0.5

os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
os.makedirs(Config.DB_DIR, exist_ok=True)