"""Document processing utilities."""

import os
import tempfile
from typing import List, Optional, Dict, Any
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

from ..models.config import settings


class DocumentProcessor:
    """Handles document loading and processing."""
    
    def __init__(self):
        """Initialize document processor."""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
    
    def process_pdf(self, file_content: bytes) -> List[Document]:
        """Process PDF file content and return document chunks."""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(file_content)
                tmp_path = tmp_file.name
            
            # Load PDF
            loader = PyPDFLoader(tmp_path)
            documents = loader.load()
            
            # Clean up temporary file
            os.unlink(tmp_path)
            
            # Split documents into chunks
            texts = self.text_splitter.split_documents(documents)
            
            return texts
            
        except Exception as e:
            raise ValueError(f"Error processing PDF: {e}")
    
    def process_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> List[Document]:
        """Process plain text and return document chunks."""
        try:
            # Create document
            document = Document(page_content=text, metadata=metadata if metadata is not None else {})
            
            # Split into chunks
            texts = self.text_splitter.split_documents([document])
            
            return texts
            
        except Exception as e:
            raise ValueError(f"Error processing text: {e}")
    
    def process_uploaded_file(self, uploaded_file) -> List[Document]:
        """Process uploaded file (Streamlit file upload object)."""
        try:
            file_content = uploaded_file.getvalue()
            
            if uploaded_file.type == "application/pdf":
                return self.process_pdf(file_content)
            else:
                # Try to decode as text
                text_content = file_content.decode('utf-8')
                metadata = {"filename": uploaded_file.name}
                return self.process_text(text_content, metadata)
                
        except Exception as e:
            raise ValueError(f"Error processing uploaded file: {e}") 