"""Base vector store interface."""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Protocol
from langchain_core.documents import Document

from ..data import DatabaseType


class BaseRetriever(Protocol):
    """Protocol for retrievers."""
    
    def get_relevant_documents(self, query: str) -> List[Document]:
        """Get relevant documents for a query."""
        ...


class BaseVectorStoreManager(ABC):
    """Abstract base class for vector store managers."""
    
    @abstractmethod
    def add_documents(self, db_type: DatabaseType, documents: List[Document]) -> None:
        """Add documents to a specific collection."""
        pass
    
    @abstractmethod
    def similarity_search_with_score(
        self, 
        db_type: DatabaseType, 
        query: str, 
        k: int = 3
    ) -> List[tuple[Document, float]]:
        """Search for similar documents with scores."""
        pass
    
    @abstractmethod
    def get_retriever(self, db_type: DatabaseType, k: int = 4) -> BaseRetriever:
        """Get retriever for a specific database."""
        pass
    
    @abstractmethod
    def search_all_databases(self, query: str, k: int = 3) -> Dict[DatabaseType, List[tuple[Document, float]]]:
        """Search all databases and return results with scores."""
        pass 