from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import tempfile

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2500,
            chunk_overlap=500,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )

    def _extract_iso_metadata(self, pages, filename: str) -> dict:

        """
        Extrae metadata específica de documentos ISO
        Args:
            pages: Lista de páginas del documento
            filename: Nombre del archivo procesado
        """
        metadata = {
            'filename': filename,
            'standard_number': None,
            'version': None,
            'sections': {}
        }
        
        # Analizar el contenido para identificar el número de estándar ISO
        first_page = pages[0].page_content
        
        # Buscar patrones ISO en el texto
        iso_pattern = r'ISO\s+\d{4,5}(?::\d{4})?'
        import re
        iso_matches = re.findall(iso_pattern, first_page)
        
        if iso_matches:
            metadata['standard_number'] = iso_matches[0]
        
        # Extraer información de secciones
        for page in pages:
            # Buscar encabezados de sección (ejemplo: "4.1", "5.2.1")
            section_pattern = r'\n(?:\d+\.)+\d+\s+[A-Z][^\n]+'
            sections = re.findall(section_pattern, page.page_content)
            
            for section in sections:
                section_num = re.findall(r'(?:\d+\.)+\d+', section)[0]
                section_title = section.replace(section_num, '').strip()
                metadata['sections'][section_num] = section_title
        
        return metadata
        
        
    def process_iso_document(self, file_obj):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(file_obj.read())
            tmp_file_path = tmp_file.name

        try:
            loader = PyPDFLoader(tmp_file_path)
            pages = loader.load()
            
            # Extract metadata with filename
            metadata = self._extract_iso_metadata(pages, file_obj.name)
            
            # Create chunks with enhanced metadata
            chunks = self.text_splitter.split_documents(pages)
            
            # Prepare the data in the format needed for Chroma
            processed_chunks = []
            chunk_metadata = []
            
            for chunk in chunks:
                # Find the corresponding section for this chunk
                section_info = self._find_section_for_chunk(chunk.page_content, metadata['sections'])
                
                processed_chunks.append(chunk.page_content)
                chunk_metadata.append({
                    'iso_standard': metadata['standard_number'],
                    'section_number': section_info['number'],
                    'section_title': section_info['title'],
                    'page': chunk.metadata.get('page', 0)
                })
            
            return processed_chunks, chunk_metadata, metadata
            
        finally:
            os.unlink(tmp_file_path)
    
    def _find_section_for_chunk(self, text: str, sections: dict) -> dict:
        """
        Identify which section a chunk belongs to
        """
        for section_num, title in sections.items():
            if section_num in text:
                return {
                    'number': section_num,
                    'title': title
                }
        return {
            'number': 'general',
            'title': 'Contenido General'
        }

    

    