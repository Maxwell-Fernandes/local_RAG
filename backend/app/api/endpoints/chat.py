"""
Chat API endpoint for conversational LAQ queries.
"""

from fastapi import APIRouter, HTTPException, Depends

from app.models.schemas import ChatQuery, ChatResponse, SearchResult
from app.services.rag import RAGService, RAGError
from app.core.dependencies import get_rag_service

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat_with_laqs(
    query: ChatQuery,
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Chat with LAQ knowledge base.

    - Retrieves relevant LAQs using semantic search
    - Generates contextual answer using LLM
    - Returns answer with source citations
    - Cites specific LAQ numbers for transparency
    """

    try:
        # Perform chat
        answer, sources = rag_service.chat(
            query=query.question,
            top_k=query.top_k
        )

        # Convert sources to response model
        source_results = [
            SearchResult(
                question=source['metadata']['question'],
                answer=source['metadata']['answer'],
                metadata=source['metadata'],
                similarity_score=source['similarity']
            )
            for source in sources
        ]

        return ChatResponse(
            question=query.question,
            answer=answer,
            sources=source_results
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RAGError as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
