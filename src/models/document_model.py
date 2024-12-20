from pydantic import BaseModel
from typing import Optional, List

class ISOSection(BaseModel):
    section_number: str
    title: str
    content: str
    parent_section: Optional[str]
    
class ISODocument(BaseModel):
    standard_number: str
    version: str
    sections: List[ISOSection]