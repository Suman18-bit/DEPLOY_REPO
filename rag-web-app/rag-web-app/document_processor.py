import os
import uuid
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import Config

class DocumentProcessor:
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
            add_start_index=True,
        )

    def process_file(self, file_path: str, original_filename: str) -> dict:
        ext = Path(original_filename).suffix.lower()
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif ext == ".txt":
            loader = TextLoader(file_path, encoding="utf-8")
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        documents = loader.load()
        for doc in documents:
            doc.metadata["source"] = original_filename
            doc.metadata["file_path"] = file_path
        chunks = self.text_splitter.split_documents(documents)
        self.vectorstore.add_documents(chunks)
        return {
            "filename": original_filename,
            "chunks": len(chunks),
            "total_chars": sum(len(c.page_content) for c in chunks),
            "status": "success"
        }

    def save_upload(self, file_content: bytes, original_filename: str) -> str:
        file_id = str(uuid.uuid4())[:8]
        safe_name = f"{file_id}_{Path(original_filename).name}"
        file_path = os.path.join(Config.UPLOAD_DIR, safe_name)
        with open(file_path, "wb") as f:
            f.write(file_content)
        return file_path, safe_name