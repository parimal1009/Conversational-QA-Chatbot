"""
Web Search Service
"""
from typing import List
from fastapi import HTTPException

from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun

from backend.config import settings
from backend.models import SearchRequest, SearchResponse


class SearchService:
    """Service for handling web search functionality"""
    
    def __init__(self):
        self.search_tools = self._initialize_search_tools()
    
    def _initialize_search_tools(self) -> List:
        """Initialize search tools for arXiv, Wikipedia, and web search"""
        tools = []
        
        # Try to add Arxiv tool
        try:
            arxiv_wrapper = ArxivAPIWrapper(
                top_k_results=settings.ARXIV_MAX_RESULTS,
                doc_content_chars_max=settings.ARXIV_MAX_CHARS
            )
            tools.append(ArxivQueryRun(api_wrapper=arxiv_wrapper, name="Academic Papers"))
        except Exception as e:
            print(f"Warning: Could not initialize ArxivQueryRun: {e}")
        
        # Try to add Wikipedia tool
        try:
            wiki_wrapper = WikipediaAPIWrapper(
                top_k_results=settings.WIKI_MAX_RESULTS,
                doc_content_chars_max=settings.WIKI_MAX_CHARS
            )
            tools.append(WikipediaQueryRun(api_wrapper=wiki_wrapper, name="Wikipedia"))
        except Exception as e:
            print(f"Warning: Could not initialize WikipediaQueryRun: {e}")
        
        # Try to add DuckDuckGo tool
        try:
            tools.append(DuckDuckGoSearchRun(name="Web Search"))
        except Exception as e:
            print(f"Warning: Could not initialize DuckDuckGoSearchRun: {e}")
        
        if not tools:
            raise Exception("No search tools could be initialized")
        
        return tools
    
    def _get_llm(self, temperature: float, max_tokens: int) -> ChatGroq:
        """Get configured LLM instance"""
        return ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            model_name=settings.MODEL_NAME,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    async def search(self, request: SearchRequest) -> SearchResponse:
        """Perform web search using multiple sources"""
        try:
            # Initialize LLM
            llm = self._get_llm(request.temperature, request.max_tokens)
            
            # Create search agent
            agent = initialize_agent(
                tools=self.search_tools,
                llm=llm,
                agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                handle_parsing_errors=True,
                verbose=False,
                max_iterations=10
            )
            
            # System message for the agent
            system_message = f"""You are an advanced AI research assistant.

Configuration:
- Model: {settings.MODEL_NAME}
- You have access to web search, academic papers (arXiv), and Wikipedia
- Provide comprehensive, well-researched answers
- Cite sources when possible
- Be accurate and precise in your responses

User query: {request.query}"""
            
            # Run agent - using invoke instead of deprecated run method
            response = agent.invoke({"input": system_message})
            
            # Extract the output from the response
            result = response.get("output", str(response))
            
            return SearchResponse(
                response=result,
                sources=["Web Search", "Academic Papers (arXiv)", "Wikipedia"]
            )
            
        except Exception as e:
            print(f"Search error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
