# Enterprise Local RAG System 🚀

A high-performance, privacy-focused Retrieval-Augmented Generation (RAG) workspace. This application allows users to upload enterprise documents (PDFs) and chat with them locally using **Ollama**, ensuring no data ever leaves the local environment.

## 🏗️ Architecture
- **Frontend**: React.js (Vite) with Tailwind CSS & Shadcn/UI for a modern Enterprise UX.
- **Backend**: FastAPI for high-performance asynchronous API handling.
- **AI Orchestration**: LangChain & `langchain_ollama`.
- **LLM**: Llama 3 (via Ollama).
- **Embeddings**: `nomic-embed-text` (Optimized for Cosine Similarity).
- **Vector Store**: ChromaDB for persistent document indexing.
- **Deployment**: Docker-ready containerization.

---

## 🛠️ Key Features
- **Local Intelligence**: Powered by Ollama for 100% data privacy.
- **Smart Ingestion**: Recursive character splitting with `nomic-embed-text` for high-accuracy retrieval.
- **Advanced Retrieval**: Cosine similarity search with adjustable relevance thresholds.
- **Modern UI**: Professional dashboard with real-time chat and document management.

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have **Ollama** installed and the models pulled:
```bash
ollama pull llama3
ollama pull nomic-embed-text
2. Backend Setup (FastAPI)
Bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
API running on: http://localhost:8000

3. Frontend Setup (React)
Bash
cd frontend
npm install
npm run dev
UI running on: http://localhost:5173

📂 Project Structure
Plaintext
enterprise-rag-system/
├── backend/
│   ├── main.py              # FastAPI Routes & RAG Logic
│   ├── chroma_db/           # Persistent Vector Storage
│   ├── uploaded_docs/       # Document Storage
│   └── requirements.txt     # Python Dependencies
├── frontend/
│   ├── src/                 # React Components (Shadcn/UI)
│   ├── tailwind.config.js   # UI Styling
│   └── vite.config.js       # Build Tooling
├── Dockerfile               # Container Configuration
└── .gitignore               # Environment Protection
🛡️ Security
This system utilizes JWT (JSON Web Tokens) and OAuth2 principles for secure enterprise access. Since it runs locally via Ollama, it is ideal for handling sensitive documents that cannot be shared with cloud-based LLM providers.

👨‍💻 Developer
Naga Poojith Ullam Full-Stack Developer & AI/ML Engineer

