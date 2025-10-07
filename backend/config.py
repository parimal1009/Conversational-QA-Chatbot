"""
Application Configuration
"""
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    APP_NAME: str = "AI Assistant Pro"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Advanced AI Assistant with PDF Chat and Web Search"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # LangSmith Configuration (Optional - for tracing)
    LANGSMITH_TRACING: str = "false"
    LANGSMITH_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGSMITH_API_KEY: str = os.getenv("LANGSMITH_API_KEY", "")
    LANGSMITH_PROJECT: str = os.getenv("LANGSMITH_PROJECT", "default")
    
    # API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    HF_TOKEN: str = os.getenv("HF_TOKEN", "")
    
    # LLM Configuration
    MODEL_NAME: str = "llama-3.3-70b-versatile"
    DEFAULT_TEMPERATURE: float = 0.3
    DEFAULT_MAX_TOKENS: int = 2048
    
    # Embedding Configuration
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DEVICE: str = "cpu"
    
    # Document Processing
    CHUNK_SIZE: int = 4000
    CHUNK_OVERLAP: int = 500
    
    # Search Configuration
    DEFAULT_SEARCH_K: int = 4
    FETCH_K_MULTIPLIER: int = 3
    MMR_LAMBDA: float = 0.5
    
    # CORS Configuration
    CORS_ORIGINS: list = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]
    
    # Search Tools Configuration
    ARXIV_MAX_RESULTS: int = 3
    ARXIV_MAX_CHARS: int = 500
    WIKI_MAX_RESULTS: int = 3
    WIKI_MAX_CHARS: int = 500
    
    class Config:
        env_file = ".env"


# Global settings instance
settings = Settings()
