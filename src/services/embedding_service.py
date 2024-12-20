from langchain_community.embeddings import CohereEmbeddings
from typing import List, Dict

class EmbeddingService:
    def __init__(self, api_key: str):
        self.embeddings = CohereEmbeddings(
            cohere_api_key=api_key,
            model="embed-multilingual-v3.0"  # Better for technical documents
        )