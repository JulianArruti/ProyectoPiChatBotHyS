from langchain_cohere import CohereEmbeddings

class EmbeddingService:
    def __init__(self, cohere_client):
        self.embeddings = CohereEmbeddings(cohere_client)
    
    def embed_documents(self, documents):
        return self.embeddings.embed_documents(documents)
    
    def embed_query(self, query):
        return self.embeddings.embed_query(query)