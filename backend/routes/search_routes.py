"""
Web Search Routes
"""
from fastapi import APIRouter

from backend.models import SearchRequest, SearchResponse
from backend.services import SearchService

router = APIRouter(prefix="/search", tags=["Web Search"])

# Initialize search service
search_service = SearchService()


@router.post("", response_model=SearchResponse)
async def web_search(request: SearchRequest):
    """
    Search the web, academic papers, and Wikipedia
    
    - **query**: Search query
    - **session_id**: Session identifier
    - **temperature**: LLM temperature (0.0-1.0)
    - **max_tokens**: Maximum response tokens
    """
    return await search_service.search(request)
