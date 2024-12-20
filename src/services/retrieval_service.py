from langchain_cohere import CohereEmbeddings
from typing import List, Optional
from src.core.vector_store import VectorStore

class RetrievalService:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        
    def contextualized_retrieval(self, query: str, session_history: List[str] = None) -> List[str]:
        """
        Realiza búsqueda contextual
        """
        return self.vector_store.similarity_search(query)