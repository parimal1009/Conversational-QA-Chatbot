"""
Pydantic Models for Request/Response Validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class ChatRequest(BaseModel):
    """Request model for PDF chat endpoint"""
    query: str = Field(..., description="User's question")
    session_id: str = Field(..., description="Unique session identifier")
    temperature: float = Field(default=0.3, ge=0.0, le=1.0, description="LLM temperature")
    max_tokens: int = Field(default=2048, ge=100, le=4096, description="Maximum tokens in response")
    search_k: int = Field(default=4, ge=1, le=10, description="Number of documents to retrieve")


class SearchRequest(BaseModel):
    """Request model for web search endpoint"""
    query: str = Field(..., description="Search query")
    session_id: str = Field(..., description="Unique session identifier")
    temperature: float = Field(default=0.3, ge=0.0, le=1.0, description="LLM temperature")
    max_tokens: int = Field(default=2048, ge=100, le=4096, description="Maximum tokens in response")


class UploadResponse(BaseModel):
    """Response model for PDF upload endpoint"""
    status: str
    processed_files: List[str]
    total_chunks: Optional[int] = None
    message: str


class SourceInfo(BaseModel):
    """Information about a source document"""
    source: str
    page: Optional[str] = None
    content: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    answer: str
    sources: Optional[List[SourceInfo]] = None
    session_id: str


class SearchResponse(BaseModel):
    """Response model for search endpoint"""
    response: str
    sources: Optional[List[str]] = None


class HealthResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str
    model: str
    timestamp: str


class SessionResponse(BaseModel):
    """Response model for session management"""
    status: str
    message: str


class SessionListResponse(BaseModel):
    """Response model for listing sessions"""
    active_sessions: List[str]
    total: int
