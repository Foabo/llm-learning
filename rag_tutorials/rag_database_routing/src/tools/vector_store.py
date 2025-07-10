"""Vector store management for Qdrant."""

from typing import Dict, List, Optional
from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from ..models import get_embedding_model
from ..models.config import settings
from ..data import DatabaseType, COLLECTIONS
from .base_vector_store import BaseVectorStoreManager


class VectorStoreManager(BaseVectorStoreManager):
    """Manages Qdrant vector store collections."""
    
    def __init__(self):
        """Initialize vector store manager."""
        if not settings.qdrant_url or not settings.qdrant_api_key:
            raise ValueError("Qdrant URL and API key are required. Please check your .env configuration.")
        
        try:
            self.client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
                timeout=30,  # 增加超时时间
                prefer_grpc=False  # 使用HTTP而不是gRPC
            )
            self.embeddings = get_embedding_model()
            self.databases: Dict[DatabaseType, QdrantVectorStore] = {}
            self._initialize_collections()
        except Exception as e:
            raise RuntimeError(f"Failed to connect to Qdrant: {str(e)}. Please check your network connection and Qdrant credentials.")
    
    def _initialize_collections(self) -> None:
        """Initialize all Qdrant collections."""
        # Test connection
        self.client.get_collections()
        
        for db_type, config in COLLECTIONS.items():
            try:
                # Try to get existing collection
                self.client.get_collection(config.collection_name)
            except Exception:
                # Create collection if it doesn't exist
                self.client.create_collection(
                    collection_name=config.collection_name,
                    vectors_config=VectorParams(
                        size=settings.vector_size, 
                        distance=Distance.COSINE
                    )
                )
            
            # Create QdrantVectorStore instance for this collection
            try:
                self.databases[db_type] = QdrantVectorStore(
                    client=self.client,
                    collection_name=config.collection_name,
                    embedding=self.embeddings
                )
            except Exception as e:
                if "dimensions" in str(e) or "force_recreate" in str(e):
                    # 维度不匹配，使用force_recreate重新创建
                    print(f"⚠️ 集合 {config.collection_name} 维度不匹配，使用force_recreate重新创建...")
                    
                    # 使用from_documents方法创建，并传递force_recreate参数
                    from langchain_core.documents import Document
                    dummy_doc = Document(page_content="dummy", metadata={})
                    
                    self.databases[db_type] = QdrantVectorStore.from_documents(
                        documents=[dummy_doc],
                        embedding=self.embeddings,
                        url=settings.qdrant_url,
                        api_key=settings.qdrant_api_key,
                        collection_name=config.collection_name,
                        force_recreate=True
                    )
                else:
                    raise e
    
    def add_documents(self, db_type: DatabaseType, documents: List[Document]) -> None:
        """Add documents to a specific collection."""
        if db_type not in self.databases:
            raise ValueError(f"Database type {db_type} not found")
        
        self.databases[db_type].add_documents(documents)
    
    def similarity_search_with_score(
        self, 
        db_type: DatabaseType, 
        query: str, 
        k: int = 3
    ) -> List[tuple[Document, float]]:
        """Search for similar documents with scores."""
        if db_type not in self.databases:
            raise ValueError(f"Database type {db_type} not found")
        
        return self.databases[db_type].similarity_search_with_score(query, k=k)
    
    def get_retriever(self, db_type: DatabaseType, k: int = 4):
        """Get retriever for a specific database."""
        if db_type not in self.databases:
            raise ValueError(f"Database type {db_type} not found")
        
        return self.databases[db_type].as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )
    
    def search_all_databases(self, query: str, k: int = 3) -> Dict[DatabaseType, List[tuple[Document, float]]]:
        """Search all databases and return results with scores."""
        results = {}
        for db_type in self.databases:
            try:
                results[db_type] = self.similarity_search_with_score(db_type, query, k)
            except Exception as e:
                print(f"Error searching {db_type}: {e}")
                results[db_type] = []
        return results 