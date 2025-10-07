"""
PDF Chat Routes
"""
from fastapi import APIRouter, UploadFile, File, Form
from typing import List

from backend.models import ChatRequest, ChatResponse, UploadResponse
from backend.services import PDFService

router = APIRouter(prefix="/pdf", tags=["PDF Chat"])

# Initialize PDF service
pdf_service = PDFService()


@router.post("/upload", response_model=UploadResponse)
async def upload_pdfs(
    files: List[UploadFile] = File(...),
    session_id: str = Form(default="default")
):
    """
    Upload and process PDF files for chat functionality
    
    - **files**: List of PDF files to upload
    - **session_id**: Unique session identifier
    """
    return await pdf_service.upload_pdfs(files, session_id)


@router.post("/chat", response_model=ChatResponse)
async def chat_with_pdfs(request: ChatRequest):
    """
    Chat with uploaded PDF documents
    
    - **query**: User's question
    - **session_id**: Session identifier
    - **temperature**: LLM temperature (0.0-1.0)
    - **max_tokens**: Maximum response tokens
    - **search_k**: Number of document chunks to retrieve
    """
    return await pdf_service.chat_with_pdfs(request)
