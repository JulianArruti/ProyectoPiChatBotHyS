from langchain_cohere import  ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_cohere import CohereRagRetriever
from langchain_cohere import CohereEmbeddings
from typing import List
import numpy as np
import os


class RAGService:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        
        self.chat_model = ChatCohere(
            model="command-r-plus-08-2024",
            temperature=0.7,
            max_tokens= 2000, #limite de cohere 4096, las respuestas de higiene y seguridad son mas largas que textos normales y restringir informacion en consejos de segurirdad no deberia ser recomendable  
            cohere_api_key=os.getenv("COHERE_API_KEY"),
        )

        self.embeddings = CohereEmbeddings(
            cohere_api_key=os.getenv("COHERE_API_KEY"),
            model="embed-multilingual-v3.0"
        )
        self.rag_retriever = CohereRagRetriever(llm=self.chat_model)

    def check_relevance(self, query: str, context: List[str], threshold: float = 0.1) -> bool:
        """
        Verifica la relevancia usando embeddings de Cohere
        """
        query_embedding = self.embeddings.embed_query(query)
        context_embeddings = self.embeddings.embed_documents(context)
        
        similarities = [
            np.dot(query_embedding, doc_embedding) / 
            (np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding))
            for doc_embedding in context_embeddings
        ]
        return max(similarities) >= threshold
        
    def generate_response(self, query: str, context: List[str], expert_advice: str) -> str:
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
            Instrucciones:
            - Eres un asistente experto en normas ISO y seguridad laboral
            - Responde en español de manera clara y profesional
            - Usa el contexto proporcionado para dar respuestas precisas
            - Incluye las advertencias de seguridad cuando sean relevantes
            
            Reglas:
            - Si la pregunta no está relacionada con el contexto, indica que no puedes responder
            - Prioriza la seguridad y las buenas prácticas
            - Cita específicamente las secciones relevantes de las normas ISO
            
            Contexto:
            {context}
            
            Advertencias de Seguridad:
            {expert_advice}
            """),
            ("user", "{query}")
        ])
        
        chain = prompt | self.chat_model | StrOutputParser()
        
        return chain.invoke({
            "context": "\n".join(context),
            "expert_advice": expert_advice,
            "query": query
        })
    
