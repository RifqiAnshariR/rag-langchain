import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from config.config import Config
from src.data_loader import load_data
from src.data_processor import DataProcessor
from src.rag_chain import RAGChainBuilder
from src.vector_store import VectorStoreManager

load_dotenv()

app = FastAPI(title="RAG API")

if os.environ.get("DOCKER"):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

try:
    processor = DataProcessor(patterns=Config.PATTERNS)
    
    vector_manager = VectorStoreManager(
        url=Config.QDRANT_URL,
        collection_name=Config.QDRANT_COLLECTION_NAME,
        model_name=Config.EMBED_MODEL_NAME
    )

    rag_builder = RAGChainBuilder(
        llm_model=Config.LLM_MODEL_NAME,
        temperature=Config.LLM_TEMPERATURE,
        system_prompt=Config.SYSTEM_PROMPT
    )

except Exception as e:
    raise

@app.get("/")
def root():
    return {"status": "RAG API is running."}

@app.on_event("startup")
async def startup_event():
    try:
        raw_data = load_data(file_path=Config.DATASET_FILE)

        preprocessed_data = processor.process(
            raw_data=raw_data, 
            chunk_size=Config.CHUNK_SIZE, 
            chunk_overlap=Config.CHUNK_OVERLAP
        )

        vector_manager.add_data(preprocessed_data)

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing file: {str(e)}"
        )

@app.post("/chat", response_model=ChatResponse)
async def chat_with_rag(request: ChatRequest):
    try:
        retriever = vector_manager.retrieve(
            search_type=Config.RETRIEVER_SEARCH_TYPE,
            search_kwargs=Config.RETRIEVER_SEARCH_KWARGS
        )

        rag_chain = rag_builder.build(retriever)
        answer = rag_chain.invoke(request.question)
        return ChatResponse(answer=answer)
    
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error generating response: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000,
        reload=True
    )
