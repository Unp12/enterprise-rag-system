import os
import shutil
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Modern LangChain Ollama Imports (Fixes Deprecation Warnings)
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

app = FastAPI(title="Enterprise Local RAG", version="2.0.0")

# --- CORS Configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Directory Configuration ---
UPLOAD_DIR = "uploaded_docs"
CHROMA_PATH = "chroma_db"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- AI Components (Local Ollama) ---
# nomic-embed-text is highly optimized for cosine similarity
embeddings = OllamaEmbeddings(model="nomic-embed-text")
llm = ChatOllama(model="llama3", temperature=0)

# --- Data Models ---
class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]

# --- API Endpoints ---

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        loader = PyPDFLoader(file_path)
        raw_docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
        )
        chunks = text_splitter.split_documents(raw_docs)

        # FIX: Explicitly set the distance metric to 'cosine' in collection_metadata
        Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=CHROMA_PATH,
            collection_metadata={"hnsw:space": "cosine"}
        )

        return {
            "message": "Local Knowledge Base Updated",
            "filename": file.filename,
            "chunks_processed": len(chunks)
        }

    except Exception as e:
        print(f"Ingestion Error: {e}")
        raise HTTPException(status_code=500, detail="Document processing failed.")

@app.post("/chat", response_model=ChatResponse)
async def chat_with_docs(request: ChatRequest):
    try:
        # Load the DB with the same 'cosine' metadata
        db = Chroma(
            persist_directory=CHROMA_PATH, 
            embedding_function=embeddings,
            collection_metadata={"hnsw:space": "cosine"}
        )

        # Perform Search
        results = db.similarity_search_with_relevance_scores(request.query, k=4)
        
        # With Cosine, scores are 0 to 1. 0.3 is a safe threshold for technical docs.
        if len(results) == 0 or results[0][1] < 0.3:
            return ChatResponse(
                answer="I couldn't find relevant information in the uploaded documents to answer that.",
                sources=[]
            )

        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        sources = list(set([doc.metadata.get("source", "Unknown") for doc, _score in results]))

        PROMPT_TEMPLATE = """
        You are a technical assistant. Use the provided context to answer the question.
        If the answer is not in the context, say you don't know.

        Context:
        {context}
        ---
        Question: {question}
        
        Answer professionally:
        """
        
        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        formatted_prompt = prompt.format(context=context_text, question=request.query)

        response = llm.invoke(formatted_prompt)

        return ChatResponse(
            answer=response.content,
            sources=sources
        )

    except Exception as e:
        print(f"Chat Error: {e}")
        raise HTTPException(status_code=500, detail="Query processing failed.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)












































































'''import os
import shutil
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# LangChain & Vector DB Imports
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables (optional now that we aren't using OpenAI)
load_dotenv()

app = FastAPI(title="Local Enterprise RAG API", version="1.5.0")

# --- CORS Configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Directory Configuration ---
UPLOAD_DIR = "uploaded_docs"
CHROMA_PATH = "chroma_db"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- UPDATED: Local AI Components (Ollama) ---
# Using nomic-embed-text for high-quality local embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")
# Using llama3 for reasoning and response generation
llm = ChatOllama(model="llama3", temperature=0)

# --- Data Models ---
class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]

# --- API Endpoints ---

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        loader = PyPDFLoader(file_path)
        raw_docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            add_start_index=True
        )
        chunks = text_splitter.split_documents(raw_docs)

        # Ingest into ChromaDB using local embeddings
        Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=CHROMA_PATH
        )

        return {
            "message": "Local Knowledge Base Updated",
            "filename": file.filename,
            "chunks_processed": len(chunks)
        }

    except Exception as e:
        print(f"Ingestion Error: {e}")
        raise HTTPException(status_code=500, detail="Document processing failed.")

@app.post("/chat", response_model=ChatResponse)
async def chat_with_docs(request: ChatRequest):
    try:
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
        results = db.similarity_search_with_relevance_scores(request.query, k=4)
        
        if len(results) == 0 or results[0][1] < 0.3: # Slightly lowered threshold for local models
            return ChatResponse(
                answer="I couldn't find enough context in the documents to answer that accurately.",
                sources=[]
            )

        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        sources = list(set([doc.metadata.get("source", "Unknown") for doc, _score in results]))

        PROMPT_TEMPLATE = """
        Use the following pieces of retrieved context to answer the question. 
        Context:
        {context}
        ---
        Question: {question}
        Answer:
        """
        
        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        formatted_prompt = prompt.format(context=context_text, question=request.query)

        response = llm.invoke(formatted_prompt)

        return ChatResponse(
            answer=response.content,
            sources=sources
        )

    except Exception as e:
        print(f"Chat Error: {e}")
        raise HTTPException(status_code=500, detail="Query processing failed.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)'''





























































































'''import os
import shutil
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# LangChain & Vector DB Imports
# 1. Update Imports
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

# Load API Keys from .env
load_dotenv()

app = FastAPI(title="Enterprise RAG API", version="1.4.0")

# --- CORS Configuration ---
# Required to allow your React frontend (port 5173) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Directory Configuration ---
UPLOAD_DIR = "uploaded_docs"
CHROMA_PATH = "chroma_db"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize AI Components
# Note: Ensure OPENAI_API_KEY is defined in your .env file
# 2. Update the AI Components (Replace the OpenAI versions)
embeddings = OllamaEmbeddings(model="nomic-embed-text")
llm = ChatOllama(model="llama3", temperature=0)

# --- Data Models ---
class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]

# --- API Endpoints ---

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Processes PDF: Loads, Chunks, and Embeds into Vector DB."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        # 1. Save file locally
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. Load and Chunk PDF
        loader = PyPDFLoader(file_path)
        raw_docs = loader.load()

        # Recursive splitting preserves paragraph/sentence structure
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            add_start_index=True
        )
        chunks = text_splitter.split_documents(raw_docs)

        # 3. Ingest into ChromaDB
        # This creates/updates the vector store in the 'chroma_db' folder
        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=CHROMA_PATH
        )

        return {
            "message": "Knowledge Base Updated",
            "filename": file.filename,
            "chunks_processed": len(chunks)
        }

    except Exception as e:
        print(f"Ingestion Error: {e}")
        raise HTTPException(status_code=500, detail="Document processing failed.")

@app.post("/chat", response_model=ChatResponse)
async def chat_with_docs(request: ChatRequest):
    """Retrieves relevant document context and generates an LLM response."""
    try:
        # 1. Initialize Vector Store
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

        # 2. Perform Similarity Search
        # Retrieve the top 4 most relevant chunks
        results = db.similarity_search_with_relevance_scores(request.query, k=4)
        
        # Filtering: If no high-confidence matches are found
        if len(results) == 0 or results[0][1] < 0.4:
            return ChatResponse(
                answer="I couldn't find specific information in the documents to answer that. Please refine your query.",
                sources=[]
            )

        # 3. Construct Context for LLM
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        sources = list(set([doc.metadata.get("source", "Unknown") for doc, _score in results]))

        # 4. Prompt Engineering (The "RAG" Secret Sauce)
        PROMPT_TEMPLATE = """
        Use the following pieces of retrieved context to answer the question. 
        If you don't know the answer based on the context, say you don't know.
        
        Context:
        {context}
        
        ---
        Question: {question}
        
        Answer professionally and concisely:
        """
        
        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        formatted_prompt = prompt.format(context=context_text, question=request.query)

        # 5. Execute LLM Call
        response = llm.invoke(formatted_prompt)

        return ChatResponse(
            answer=response.content,
            sources=sources
        )

    except Exception as e:
        print(f"Chat Error: {e}")
        raise HTTPException(status_code=500, detail="Query processing failed.")

if __name__ == "__main__":
    import uvicorn
    # Port 8000 matches your frontend's fetch requests
    uvicorn.run(app, host="0.0.0.0", port=8000)'''