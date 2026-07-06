<div align="center">

# 📚 AskMyBook

**Turn any document into a conversation.**

Upload a PDF or text file and ask it questions — get answers grounded in exactly what's on the page, with the source passages to prove it.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-1C3C3C?style=flat-square)](https://www.langchain.com/)
[![Mistral AI](https://img.shields.io/badge/Mistral_AI-Powered-FA520F?style=flat-square)](https://mistral.ai/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-6B4FBB?style=flat-square)](https://www.trychroma.com/)
[![Vercel](https://img.shields.io/badge/Deploy-Vercel-000000?style=flat-square&logo=vercel&logoColor=white)](https://vercel.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

</div>

---

## ✨ Overview

**AskMyBook** is a Retrieval-Augmented Generation (RAG) web app. Drop in a PDF or `.txt` file and it's chunked, embedded, and stored in a vector database. From there you can chat with it directly — every answer is built only from what's actually in the document, and comes with the exact source snippets it was drawn from, so you never have to take the model's word for it.

## 🖼️ Preview

*Add a screenshot or short GIF of the chat interface here — it's the single highest-impact addition you can make to this README.*

## 🚀 Features

- **📤 Drag-and-drop uploads** for PDF and TXT files, with a live progress indicator
- **💬 Natural-language Q&A** over your uploaded document
- **🔍 Source-grounded answers** — every response cites the passages it came from
- **🧠 Hallucination-resistant by design** — the model is instructed to say *"I don't know based on the given context"* instead of guessing
- **🎯 MMR retrieval** — Maximal Marginal Relevance balances relevance and diversity across retrieved chunks
- **📊 Live sidebar stats** — active model, connection status, and documents indexed
- **☁️ Serverless-ready** — dual entry points so the app runs identically on your machine or on Vercel

## 🏗️ How It Works

1. **Upload** a PDF or `.txt` file from the sidebar.
2. **Chunk** — the document is split into ~1,000-character pieces with 200-character overlap.
3. **Embed & store** — each chunk is embedded with Mistral's `mistral-embed` model and saved to a **ChromaDB** vector store.
4. **Ask** a question in the chat box.
5. **Retrieve** — an MMR search (`k=3`, `fetch_k=10`, `λ=0.5`) pulls the most relevant, non-redundant chunks.
6. **Generate** — the retrieved context and your question go to Mistral's `mistral-small` model under a strict "context-only" system prompt.
7. **Answer** — you get a grounded response plus the exact source excerpts behind it.

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Uvicorn |
| LLM | Mistral AI — `mistral-small` (via `langchain-mistralai`) |
| Embeddings | Mistral AI — `mistral-embed` |
| Vector store | ChromaDB (via `langchain-chroma`) |
| Document parsing | `pypdf`, LangChain community loaders |
| Chunking | LangChain `RecursiveCharacterTextSplitter` |
| Frontend | HTML, CSS, vanilla JS |
| Deployment | Vercel (`@vercel/python`) |

## 📁 Project Structure

```
rag-web-app/
├── api.py                  # FastAPI app entry point (local dev)
├── api/
│   └── index.py             # Vercel serverless entry point
├── config.py                # Models, chunking & retriever settings
├── document_processor.py    # Loads, chunks, and indexes uploads
├── rag_engine.py             # Embeddings, retrieval & answer generation
├── templates/
│   └── index.html             # Chat UI
├── static/                    # Assets served in local dev
├── public/static/             # Assets served on Vercel
├── requirements.txt
└── vercel.json
```

## ⚙️ Getting Started

### Prerequisites
- Python 3.10+
- A [Mistral AI API key](https://console.mistral.ai/)

### Installation

```bash
git clone https://github.com/Suman18-bit/DEPLOY_REPO.git
cd DEPLOY_REPO/rag-web-app

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Configure

Create a `.env` file inside `rag-web-app/`:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
```

### Run

```bash
python api.py
# or
uvicorn api:app --reload --port 8000
```

Open **http://localhost:8000** in your browser.

## 📖 Usage

1. Drag a PDF or `.txt` file into the upload zone (or click to browse).
2. Wait for the "uploaded and indexed successfully" confirmation.
3. Ask a question about the document in the chat box.
4. Check the cited sources alongside the answer to verify it yourself.

## 🔌 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the chat UI |
| `POST` | `/upload` | Upload and index a `.pdf` or `.txt` file |
| `POST` | `/chat` | Ask a question → `{ answer, sources }` |
| `GET` | `/health` | Health check → app status and active model |

<details>
<summary><strong>Example requests</strong></summary>

**Upload a document**
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@mybook.pdf"
```

**Ask a question**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main argument of chapter 2?"}'
```

</details>

## ☁️ Deployment

This repo ships ready for **Vercel**:

```bash
vercel --prod
```

Set `MISTRAL_API_KEY` as an environment variable in your Vercel project settings. `vercel.json` routes all traffic through `api/index.py` and serves static files from `public/static/`.

> [!WARNING]
> Vercel's serverless filesystem only allows writes to `/tmp`, and `/tmp` isn't guaranteed to persist between invocations. That's fine for a demo, but for production use, point `DB_DIR` at a hosted vector store (e.g. Chroma Cloud, Pinecone, or Qdrant) instead of local disk.

## 🎛️ Configuration Reference

All tunable values live in `config.py`:

| Setting | Default | Description |
|---|---|---|
| `EMBEDDING_MODEL` | `mistral-embed` | Embedding model |
| `LLM_MODEL` | `mistral-small` | Chat/generation model |
| `CHUNK_SIZE` | `1000` | Characters per chunk |
| `CHUNK_OVERLAP` | `200` | Overlap between chunks |
| `RETRIEVER_K` | `3` | Chunks returned per query |
| `RETRIEVER_FETCH_K` | `10` | Candidates considered before MMR filtering |
| `RETRIEVER_LAMBDA` | `0.5` | Relevance vs. diversity balance |

## 🗺️ Roadmap

- [ ] Per-document / per-session isolation (all uploads currently share one knowledge base)
- [ ] Conversation memory across turns
- [ ] Support for `.epub` and `.docx` uploads
- [ ] Streaming responses
- [ ] Ability to delete or reset indexed documents

## 🤝 Contributing

Issues and pull requests are welcome. If you spot a bug or have an idea for a feature, feel free to open one.

## 📄 License

MIT — see [LICENSE](LICENSE) for details.

## 🙌 Acknowledgments

- [Mistral AI](https://mistral.ai/) for the LLM and embeddings
- [LangChain](https://www.langchain.com/) for RAG orchestration
- [Chroma](https://www.trychroma.com/) for vector storage

---

<div align="center">
Built by <a href="https://github.com/Suman18-bit">Suman Seth</a>
</div>
