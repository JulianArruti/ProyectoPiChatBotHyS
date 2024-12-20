import os
from typing import List
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
import cohere
from src.core.document_processor import DocumentProcessor
from src.core.vector_store import VectorStore
from src.services.retrieval_service import RetrievalService
from src.services.contextualization import Contextualization
from src.services.rag_service import RAGService
from dotenv import load_dotenv
import io

app = FastAPI()

load_dotenv()
cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))
document_processor = DocumentProcessor()
vector_store = VectorStore(
    persist_directory="data/processed/",
    cohere_client=cohere_client
)

retrieval = RetrievalService(vector_store)

# Deberian generarse para cada documento, ya que el aporte de un profesional del área mejoraria la funcionalidad (lo hice con lo que me acuerdo de Higiene y Seguridad de mi facu y viendo los pdfs)
contextualization = Contextualization(safety_rules={
    "PPE": "Siempre use el equipo de protección personal apropiado.",
    "Procedimientos de Emergencia": "Siga los procedimientos de emergencia del manual de seguridad.",
    "Identificación de peligros": "Identifique y evalúe de manera proactiva los peligros en el lugar de trabajo.",
    "Reportes de incidentes": "Reporte todos los incidentes, incluidos los cuasi-accidentes, de manera inmediata.",
    "Evaluación de riesgos": "Realice evaluaciones de riesgos periódicas para mitigar peligros potenciales.",
    "Gestión del cambio": "Evalúe y controle los riesgos asociados a cambios en procesos, equipos o personal.",
})

rag_service = RAGService(vector_store)
class QueryRequest(BaseModel):
    query: str


@app.post("/checking the document")
async def test_document_processing(file: UploadFile = File(...)):
    """
    Test endpoint to verify new document processing structure before ChromaDB storage
    """
    if not file.filename.endswith('.pdf'):
        return {"error": "Please upload a PDF file"}
    
    # Get the file content
    file_content = await file.read()
    file_obj = io.BytesIO(file_content)
    file_obj.name = file.filename
    
    # Process document with new structure
    chunks, chunk_metadata, doc_metadata = document_processor.process_iso_document(file_obj)
    
    # Generate sample IDs for visualization
    chunk_ids = [f"{doc_metadata['standard_number']}_chunk_{i}" for i in range(len(chunks))]
    
    # Prepare sample data structure (showing first 3 chunks)
    sample_data = []
    for i in range(min(3, len(chunks))):
        sample_data.append({
            "id": chunk_ids[i],
            "text": chunks[i][:200] + "...",  # First 200 chars
            "metadata": chunk_metadata[i]
        })
    
    return {
        "document_info": {
            "filename": file.filename,
            "iso_standard": doc_metadata['standard_number'],
            "total_chunks": len(chunks),
            "total_sections": len(doc_metadata['sections'])
        },
        "sample_chunks": sample_data,
        "document_metadata": doc_metadata,
        "data_structure": {
            "chunks_type": str(type(chunks)),
            "metadata_type": str(type(chunk_metadata)),
            "total_metadata_fields": len(chunk_metadata[0]) if chunk_metadata else 0
        }
    }

@app.post("/upload_document")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        return {"error": "Please upload a PDF file"}
    
    file_content = await file.read()
    file_obj = io.BytesIO(file_content)
    file_obj.name = file.filename
    
    # Get processed chunks and metadata
    chunks, chunk_metadata, doc_metadata = document_processor.process_iso_document(file_obj)
    
    # Generate unique IDs for each chunk
    chunk_ids = [f"{doc_metadata['standard_number']}_chunk_{i}" for i in range(len(chunks))]
    
    # Add to vector store using the native Chroma format
    vector_store.add_documents(
        texts=chunks,  # Ya son strings
        metadatas=chunk_metadata,  # Ya son diccionarios
        ids=chunk_ids
    )
    
    return {
        "message": f"Successfully processed and added {len(chunks)} chunks from {file.filename}",
        "document_metadata": doc_metadata,
        "total_chunks": len(chunks)
    }

@app.get("/stored_documents")
async def get_stored_documents():
    """
    Endpoint para consultar los documentos ISO almacenados
    """
    stored_docs = vector_store.get_stored_documents()
    
    return {
        "total_documents": len(stored_docs),
        "documents": stored_docs
    }

@app.post("/query_documents")
async def query_documents(request: QueryRequest):
    query = request.query
    results = retrieval.contextualized_retrieval(query)
    return {"results": results}

@app.post("/ask_question")
async def ask_question(request: QueryRequest):
    question = request.query
    
    # Obtener resultados y embeddings
    results = retrieval.contextualized_retrieval(question)
    
    # Verificar relevancia
    if not rag_service.check_relevance(question, results):
        return {
            "answer": "Lo siento, no tengo información relevante para responder esta pregunta."
        }
    
    # Obtener consejos de seguridad
    expert_advice = "\n".join(
        contextualization.check_expert_system(result)
        for result in results
        if contextualization.check_expert_system(result)
    )
    
    # Generar respuesta usando RAG
    response = rag_service.generate_response(
        query=question,
        context=results,
        expert_advice=expert_advice
    )
    
    return {
        "answer": response,
        "context_used": results,
        "expert_advice": expert_advice if expert_advice else None
    }



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)