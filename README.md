Enterprise RAG System 🚀
A high-performance, local-first Retrieval-Augmented Generation (RAG) system built with FastAPI, React, and Ollama. This workspace provides a secure environment for document intelligence without relying on external LLM APIs.

🛠 Tech Stack
Frontend
Framework: React.js (Vite)

Styling: Tailwind CSS + Shadcn/UI

State Management: Hooks & Fetch API

Backend (Core Engine)
Framework: FastAPI (Python)

Orchestration: LangChain (using langchain_ollama)

LLM: Llama 3 (via Ollama)

Embeddings: Nomic-Embed-Text (Optimized for Cosine Similarity)

Vector Database: ChromaDB

Infrastructure
Containerization: Docker (Deployment ready)

Security: JWT & OAuth2 integration ready

🏗 System Architecture
Ingestion: PDF documents are uploaded, chunked using RecursiveCharacterTextSplitter, and converted into vectors.

Storage: Vectors are stored in a local ChromaDB instance with a cosine distance metric.

Retrieval: User queries are embedded and compared against the vector store using similarity search.

Generation: The retrieved context and original query are passed to Llama 3 to generate a grounded, professional response.

🚀 Getting Started
Prerequisites
Ollama Installed: Download here

Pull Required Models:

Bash
ollama pull llama3
ollama pull nomic-embed-text
Backend Setup
Navigate to the backend folder:

Bash
cd backend
Install dependencies:

Bash
pip install -r requirements.txt
Run the server:

Bash
python main.py
The API will be available at http://localhost:8000

Frontend Setup
Navigate to the frontend folder:

Bash
cd frontend
Install dependencies:

Bash
npm install
Start the development server:

Bash
npm run dev
The UI will be available at http://localhost:5173

📂 Project Structure
Plaintext
enterprise-rag-system/
├── backend/            # FastAPI, LangChain, ChromaDB
├── frontend/           # React, Tailwind, Shadcn components
├── uploaded_docs/      # Local storage for processed PDFs
├── chroma_db/          # Persistent vector storage
└── docker-compose.yml  # Multi-container orchestration
🛡 Security & Privacy
Because this system utilizes Ollama, all data stays on your local machine or private server. No document content or queries are ever sent to third-party providers like OpenAI or Anthropic.

One final tip:
Make sure your requirements.txt in the backend folder includes langchain-ollama, langchain-chroma, and pypdf so that anyone cloning the repo can get started immediately.
