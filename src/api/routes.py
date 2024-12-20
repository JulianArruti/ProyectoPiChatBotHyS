from fastapi import APIRouter
from src.services.embedding_service import EmbeddingService
from src.services.retrieval_service import RetrievalService
from src.core.vector_store import VectorStore
from typing import List  # Add this import

router = APIRouter()

embedding_service = EmbeddingService(api_key="YOUR_COHERE_API_KEY")
vector_store = VectorStore(persist_directory="data/processed/")
retrieval_service = RetrievalService(vector_store)

@router.post("/embed/")
async def embed_documents(texts: List[str]):
    embeddings = embedding_service.generate_embeddings(texts)
    vector_store.add_documents(texts, embeddings)
    return {"message": "Documents embedded successfully."}

@router.post("/retrieve/")
async def retrieve_documents(query: str):
    results = retrieval_service.retrieve_relevant_documents(query)
    return {"results": results}