"""
Search API endpoint for semantic LAQ search.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Optional

from app.models.schemas import SearchQuery, SearchResponse, SearchResult
from app.services.rag import RAGService, RAGError
from app.core.dependencies import get_rag_service

router = APIRouter()


@router.post("/", response_model=SearchResponse)
async def search_laqs(
    query: SearchQuery,
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Perform semantic search on LAQ database.

    - Generates query embedding
    - Retrieves relevant LAQs with query expansion
    - Returns ranked results with similarity scores
    - Supports filtering by threshold
    """

    try:
        # Perform search with optional threshold filtering
        apply_threshold = query.threshold is not None
        results = rag_service.search(
            query=query.query,
            top_k=query.top_k,
            apply_threshold=apply_threshold
        )

        # Convert to response model
        search_results = [
            SearchResult(
                question=result['metadata']['question'],
                answer=result['metadata']['answer'],
                metadata=result['metadata'],
                similarity_score=result['similarity']
            )
            for result in results
        ]

        return SearchResponse(
            query=query.query,
            results=search_results,
            total_results=len(search_results)
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RAGError as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
