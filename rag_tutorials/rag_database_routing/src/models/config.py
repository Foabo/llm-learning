"""Configuration management using Pydantic Settings."""

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration (兼容OpenRouter和豆包)
    openai_api_key: Optional[str] = Field(default="your_openai_api_key_here", description="OpenAI API key")
    openai_base_url: Optional[str] = Field(default=None, description="OpenAI base URL")
    openai_model: str = Field(default="gpt-4o", description="OpenAI model to use")
    embedding_model: str = Field(default="text-embedding-3-small", description="Embedding model")
    
    # 豆包/ARK Configuration
    ark_api_key: Optional[str] = Field(default=None, description="ARK API key for 豆包")
    ark_base_url: Optional[str] = Field(default=None, description="ARK base URL for 豆包")
    doubao_embedding_model: Optional[str] = Field(default=None, description="豆包 embedding model")
    
    # Qdrant Configuration  
    qdrant_url: Optional[str] = Field(default=None, description="Qdrant cluster URL")
    qdrant_api_key: Optional[str] = Field(default=None, description="Qdrant API key")
    
    # Application Settings
    debug: bool = Field(default=False, description="Debug mode")
    log_level: str = Field(default="INFO", description="Logging level")
    
    # Vector Store Settings
    vector_size: int = Field(default=1536, description="Vector dimension size")
    similarity_threshold: float = Field(default=0.5, description="Similarity threshold for routing")
    chunk_size: int = Field(default=1000, description="Text chunk size")
    chunk_overlap: int = Field(default=200, description="Text chunk overlap")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings() 