from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from pathlib import Path

from config import Config
from rag_engine import RAGEngine
from document_processor import DocumentProcessor

app = FastAPI(title="RAG Web App", version="1.0")

rag_engine = RAGEngine()
doc_processor = DocumentProcessor(rag_engine.get_vectorstore())

app.mount("/static", StaticFiles(directory="static"), name="static")

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[dict]

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("templates/index.html", "r", encoding="utf-8") as f:
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)