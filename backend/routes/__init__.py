"""
Routes Package
"""
from .pdf_routes import router as pdf_router
from .search_routes import router as search_router
from .system_routes import router as system_router

__all__ = ['pdf_router', 'search_router', 'system_router']
