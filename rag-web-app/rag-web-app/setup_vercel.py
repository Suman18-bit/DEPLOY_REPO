"""
Vercel Deployment Fix Script
Run this to restructure your project correctly for Vercel Python deployment.
"""

import os
import shutil

BASE_DIR = r"B:\AI\rag-web-app"

print("="*60)
print("VERCEL DEPLOYMENT FIX")
print("="*60)
print()

# Step 1: Check current structure
print("Step 1: Checking current structure...")
if os.path.exists(os.path.join(BASE_DIR, "api", "index.py")):
    print("  Found: api/index.py (WRONG - needs to be at root)")
else:
    print("  api/index.py not found")

if os.path.exists(os.path.join(BASE_DIR, "index.py")):
    print("  Found: index.py at root (CORRECT)")
else:
    print("  index.py at root NOT FOUND")

print()

# Step 2: Create correct index.py at root
print("Step 2: Creating correct index.py at root...")

index_py_content = """import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from pathlib import Path

from config import Config
from rag_engine import RAGEngine
from document_processor import DocumentProcessor

# Vercel Python runtime looks for 'app' at module level
app = FastAPI(title="RAG Web App", version="1.0")

rag_engine = RAGEngine()
doc_processor = DocumentProcessor(rag_engine.get_vectorstore())

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="public/static"), name="static")
except Exception as e:
    print(f"Static files mount warning: {e}")

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[dict]

@app.get("/", response_class=HTMLResponse)
async def read_root():
    template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result = rag_engine.ask(request.question)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    allowed_ext = {".pdf", ".txt"}
    ext = Path(file.filename).suffix.lower()
    if ext not in allowed_ext:
        raise HTTPException(status_code=400, detail=f"Only {', '.join(allowed_ext)} files are allowed")
    try:
        content = await file.read()
        file_path, safe_name = doc_processor.save_upload(content, file.filename)
        result = doc_processor.process_file(file_path, file.filename)
        return {"message": "File uploaded and indexed successfully", "details": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok", "model": Config.LLM_MODEL}
"""

index_path = os.path.join(BASE_DIR, "index.py")
with open(index_path, 'w') as f:
    f.write(index_py_content)
print(f"  Created: {index_path}")

# Step 3: Update vercel.json
print("Step 3: Updating vercel.json...")

vercel_json_content = """{
  "version": 2,
  "builds": [
    {
      "src": "index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/public/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/index"
    }
  ]
}
"""

vercel_path = os.path.join(BASE_DIR, "vercel.json")
with open(vercel_path, 'w') as f:
    f.write(vercel_json_content)
print(f"  Updated: {vercel_path}")

# Step 4: Update config.py for Vercel
print("Step 4: Updating config.py for Vercel...")

config_content = """import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    # Vercel uses /tmp (ephemeral storage)
    UPLOAD_DIR = "/tmp/uploads"
    DB_DIR = "/tmp/db"
    EMBEDDING_MODEL = "mistral-embed"
    LLM_MODEL = "mistral-small"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    RETRIEVER_K = 3
    RETRIEVER_FETCH_K = 10
    RETRIEVER_LAMBDA = 0.5

os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
os.makedirs(Config.DB_DIR, exist_ok=True)
"""

config_path = os.path.join(BASE_DIR, "config.py")
with open(config_path, 'w') as f:
    f.write(config_content)
print(f"  Updated: {config_path}")

# Step 5: Update requirements.txt (lightweight)
print("Step 5: Updating requirements.txt...")

requirements_content = """fastapi
uvicorn
python-multipart
pydantic
python-dotenv
langchain-core
langchain-mistralai
langchain-text-splitters
langchain-community
langchain-chroma
chromadb
pypdf
"""

req_path = os.path.join(BASE_DIR, "requirements.txt")
with open(req_path, 'w') as f:
    f.write(requirements_content)
print(f"  Updated: {req_path}")

# Step 6: Ensure public/static/ exists with files
print("Step 6: Checking public/static/...")
public_css = os.path.join(BASE_DIR, "public", "static", "css")
public_js = os.path.join(BASE_DIR, "public", "static", "js")
os.makedirs(public_css, exist_ok=True)
os.makedirs(public_js, exist_ok=True)

# Copy from static/ to public/static/ if needed
static_css = os.path.join(BASE_DIR, "static", "css", "style.css")
static_js = os.path.join(BASE_DIR, "static", "js", "app.js")

if os.path.exists(static_css):
    shutil.copy2(static_css, os.path.join(public_css, "style.css"))
    print(f"  Copied: style.css -> public/static/css/")
else:
    print(f"  WARNING: {static_css} not found!")

if os.path.exists(static_js):
    shutil.copy2(static_js, os.path.join(public_js, "app.js"))
    print(f"  Copied: app.js -> public/static/js/")
else:
    print(f"  WARNING: {static_js} not found!")

print()
print("="*60)
print("SETUP COMPLETE!")
print("="*60)
print("""
Your project is now correctly structured for Vercel.

FINAL STRUCTURE:
rag-web-app/
├── index.py          ← NEW (root level entry point)
├── api.py            ← (local development - keep it)
├── config.py         ← UPDATED
├── rag_engine.py
├── document_processor.py
├── requirements.txt  ← UPDATED
├── vercel.json       ← UPDATED
├── templates/
│   └── index.html
├── static/           ← (for local dev)
│   ├── css/
│   └── js/
└── public/           ← (for Vercel static files)
    └── static/
        ├── css/
        └── js/

NEXT STEPS:
1. Delete the api/ folder (no longer needed):
   rd /s /q B:\AI\rag-web-app\api

2. Commit and push to GitHub:
   git add .
   git commit -m "Fix Vercel deployment structure"
   git push origin main

3. Vercel will auto-deploy!

4. If still 404, check Vercel Dashboard > Functions tab for errors.
""")