from langchain_chroma import Chroma  
from typing import List, Dict, Optional
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_cohere import CohereEmbeddings
import os 

class VectorStore:
    def __init__(self, persist_directory: str, cohere_client):
        self.embeddings = CohereEmbeddings(
            cohere_api_key=os.getenv("COHERE_API_KEY"),
            model="embed-multilingual-v3.0"
        )
        
        self.vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings,
            collection_name="iso_standards"
        )

    def add_documents(self, texts: List[str], metadatas: List[Dict], ids: List[str] = None) -> None:
        """
        Add documents to the vector store with proper metadata
        """
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in texts]
            
        self.vectorstore.add_texts(
            texts=texts,
            metadatas=metadatas,
            ids=ids
        )
        
    def similarity_search(self, query: str, k: int = 4) -> List[str]:
        """
        Realiza búsqueda de similitud en el vector store
        """
        results = self.vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in results]
    
    def get_stored_documents(self) -> List[Dict]:
        """
        Obtiene un listado de documentos ISO almacenados
        """
        # Obtener todos los metadatos
        results = self.vectorstore.get()
        
        # Extraer documentos únicos basados en iso_standard
        stored_docs = set()
        documents_info = []
        
        if results and results['metadatas']:
            for metadata in results['metadatas']:
                if metadata['iso_standard'] not in stored_docs:
                    stored_docs.add(metadata['iso_standard'])
                    documents_info.append({
                        'iso_standard': metadata['iso_standard'],
                        'total_chunks': len([m for m in results['metadatas'] 
                                          if m['iso_standard'] == metadata['iso_standard']])
                    })
        
        return documents_info