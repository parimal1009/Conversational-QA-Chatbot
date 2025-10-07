"""
System Routes (Health Check, Session Management)
"""
from fastapi import APIRouter
from datetime import datetime

from backend.models import HealthResponse, SessionResponse, SessionListResponse
from backend.config import settings
from backend.routes.pdf_routes import pdf_service

router = APIRouter(tags=["System"])


@router.get("/", response_model=dict)
async def root():
    """Root endpoint with API information"""
    return {
        "message": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": settings.APP_DESCRIPTION,
        "endpoints": {
            "upload": "/pdf/upload",
            "chat": "/pdf/chat",
            "search": "/search",
            "health": "/health",
            "sessions": "/sessions"
        }
    }


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        model=settings.MODEL_NAME,
        timestamp=datetime.now().isoformat()
    )


@router.get("/sessions", response_model=SessionListResponse)
async def list_sessions():
    """List all active sessions"""
    active_sessions = pdf_service.get_active_sessions()
    return SessionListResponse(
        active_sessions=active_sessions,
        total=len(active_sessions)
    )


@router.delete("/session/{session_id}", response_model=SessionResponse)
async def clear_session(session_id: str):
    """
    Clear session data including chat history and vector store
    
    - **session_id**: Session identifier to clear
    """
    pdf_service.clear_session(session_id)
    return SessionResponse(
        status="success",
        message=f"Session {session_id} cleared"
    )
