"""
Dependency injection for FastAPI endpoints.
"""

from functools import lru_cache
from app.services.config import Config
from app.services.database import LAQDatabase
from app.services.embeddings import EmbeddingService
from app.services.rag import RAGService


@lru_cache()
def get_config() -> Config:
    """Get cached configuration instance."""
    return Config()


def get_database() -> LAQDatabase:
    """Get database instance."""
    config = get_config()
    return LAQDatabase(config)


def get_embedding_service() -> EmbeddingService:
    """Get embedding service instance."""
    config = get_config()
    return EmbeddingService(config)


def get_rag_service() -> RAGService:
    """Get RAG service instance with all dependencies."""
    config = get_config()
    database = get_database()
    embedding_service = get_embedding_service()
    return RAGService(config, database, embedding_service)
