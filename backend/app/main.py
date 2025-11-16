"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.endpoints import upload, search, chat, database
from app.core.dependencies import get_config


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print("🚀 Starting LAQ RAG System...")
    config = get_config()
    print(f"✅ Configuration loaded")
    print(f"   - Database: {config.db_path}")
    print(f"   - LLM: {config.llm_model}")
    print(f"   - Embeddings: {config.embedding_model}")

    yield

    # Shutdown
    print("👋 Shutting down LAQ RAG System...")


# Create FastAPI app
app = FastAPI(
    title="LAQ RAG System",
    description="Privacy-friendly RAG system for Legislative Assembly Questions",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(search.router, prefix="/api/search", tags=["Search"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(database.router, prefix="/api/database", tags=["Database"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "LAQ RAG System API",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    from app.services.config import Config
    from app.services.embeddings import EmbeddingService, OllamaConnectionError

    config = Config()
    status = "healthy"
    ollama_running = True
    database_status = "connected"

    try:
        # Check Ollama connection
        embedding_service = EmbeddingService(config)
        ollama_running = True
    except OllamaConnectionError:
        ollama_running = False
        status = "degraded"
    except Exception as e:
        ollama_running = False
        status = "unhealthy"
        database_status = f"error: {str(e)}"

    return {
        "status": status,
        "ollama_running": ollama_running,
        "database": database_status,
        "config": {
            "llm_model": config.llm_model,
            "embedding_model": config.embedding_model,
            "db_path": str(config.db_path)
        }
    }
