from pydantic import BaseModel
from typing import List, Optional

class DocumentUploadRequest(BaseModel):
    source: Optional[str] = None

class QueryRequest(BaseModel):
    query: str

class DocumentResponse(BaseModel):
    documents: List[str]
    metadata: Optional[dict] = None

class RAGResponse(BaseModel):
    results: List[str]
    expert_advice: str