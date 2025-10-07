"""
PDF Processing and Chat Service
"""
import os
import tempfile
import hashlib
from typing import Dict, List, Set
from fastapi import UploadFile, HTTPException

from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from backend.config import settings
from backend.models import ChatRequest, UploadResponse, ChatResponse, SourceInfo


class PDFService:
    """Service for handling PDF processing and chat functionality"""
    
    def __init__(self):
        self.vector_stores: Dict[str, FAISS] = {}
        self.chat_histories: Dict[str, ChatMessageHistory] = {}
        self.processed_files: Dict[str, Set] = {}
        self.embeddings = self._initialize_embeddings()
    
    def _initialize_embeddings(self) -> HuggingFaceEmbeddings:
        """Initialize HuggingFace embeddings"""
        return HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={'device': settings.EMBEDDING_DEVICE},
            encode_kwargs={'normalize_embeddings': True}
        )
    
    def _get_llm(self, temperature: float, max_tokens: int) -> ChatGroq:
        """Get configured LLM instance"""
        return ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            model_name=settings.MODEL_NAME,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    def _get_file_hash(self, content: bytes) -> str:
        """Generate MD5 hash of file content"""
        return hashlib.md5(content).hexdigest()
    
    def _get_session_history(self, session_id: str) -> ChatMessageHistory:
        """Get or create chat history for session"""
        if session_id not in self.chat_histories:
            self.chat_histories[session_id] = ChatMessageHistory()
        return self.chat_histories[session_id]
    
    async def upload_pdfs(
        self, 
        files: List[UploadFile], 
        session_id: str
    ) -> UploadResponse:
        """Process and upload PDF files"""
        try:
            if session_id not in self.processed_files:
                self.processed_files[session_id] = set()
            
            documents = []
            new_files = []
            
            for file in files:
                if not file.filename.endswith('.pdf'):
                    continue
                
                content = await file.read()
                file_hash = self._get_file_hash(content)
                
                if file_hash not in self.processed_files[session_id]:
                    # Save to temporary file
                    with tempfile.NamedTemporaryFile(
                        delete=False, 
                        suffix=".pdf"
                    ) as temp_file:
                        temp_file.write(content)
                        temp_path = temp_file.name
                    
                    try:
                        # Load and process PDF
                        loader = PyMuPDFLoader(temp_path)
                        docs = loader.load()
                        documents.extend(docs)
                        
                        self.processed_files[session_id].add(file_hash)
                        new_files.append(file.filename)
                    finally:
                        # Cleanup temp file
                        os.unlink(temp_path)
            
            if not documents:
                return UploadResponse(
                    status="no_new_files",
                    processed_files=[],
                    message="All files were already processed"
                )
            
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP,
                separators=["\n\n", "\n", ". ", " ", ""],
                length_function=len
            )
            
            splits = text_splitter.split_documents(documents)
            
            # Create or update vector store
            if session_id not in self.vector_stores:
                self.vector_stores[session_id] = FAISS.from_documents(
                    splits, 
                    self.embeddings
                )
            else:
                self.vector_stores[session_id].add_documents(splits)
            
            return UploadResponse(
                status="success",
                processed_files=new_files,
                total_chunks=len(splits),
                message=f"Successfully processed {len(new_files)} PDF(s)"
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def chat_with_pdfs(self, request: ChatRequest) -> ChatResponse:
        """Chat with uploaded PDF documents"""
        try:
            if request.session_id not in self.vector_stores:
                raise HTTPException(
                    status_code=400,
                    detail="No documents uploaded. Please upload PDFs first."
                )
            
            # Initialize LLM
            llm = self._get_llm(request.temperature, request.max_tokens)
            
            # Setup retriever with MMR search
            retriever = self.vector_stores[request.session_id].as_retriever(
                search_type="mmr",
                search_kwargs={
                    "k": request.search_k,
                    "fetch_k": min(20, request.search_k * settings.FETCH_K_MULTIPLIER),
                    "lambda_mult": settings.MMR_LAMBDA
                }
            )
            
            # Contextualize question prompt
            contextualize_q_system_prompt = """You are an expert at understanding questions in context.
Reformulate the question to be standalone and clear, preserving all intent.
Do not answer the question - only clarify it."""
            
            contextualize_q_prompt = ChatPromptTemplate.from_messages([
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ])
            
            history_aware_retriever = create_history_aware_retriever(
                llm, retriever, contextualize_q_prompt
            )
            
            # QA prompt
            qa_system_prompt = """You are an expert research assistant analyzing documents.

Guidelines:
1. Provide precise, professional answers based only on the provided context
2. Cite sources with page numbers when possible
3. If information is not in the documents, clearly state that
4. Break complex answers into clear paragraphs
5. Maintain conversation context

Context:
{context}"""
            
            qa_prompt = ChatPromptTemplate.from_messages([
                ("system", qa_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ])
            
            # Create chains
            question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
            rag_chain = create_retrieval_chain(
                history_aware_retriever, 
                question_answer_chain
            )
            
            conversational_rag_chain = RunnableWithMessageHistory(
                rag_chain,
                self._get_session_history,
                input_messages_key="input",
                history_messages_key="chat_history",
                output_messages_key="answer"
            )
            
            # Generate response
            response = conversational_rag_chain.invoke(
                {"input": request.query},
                config={"configurable": {"session_id": request.session_id}}
            )
            
            # Extract sources
            sources = []
            if 'context' in response:
                for doc in response['context']:
                    sources.append(SourceInfo(
                        source=os.path.basename(doc.metadata.get('source', 'Unknown')),
                        page=str(doc.metadata.get('page', 'N/A')),
                        content=doc.page_content[:200] + "..."
                    ))
            
            return ChatResponse(
                answer=response['answer'],
                sources=sources,
                session_id=request.session_id
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def clear_session(self, session_id: str) -> None:
        """Clear session data"""
        if session_id in self.chat_histories:
            del self.chat_histories[session_id]
        if session_id in self.vector_stores:
            del self.vector_stores[session_id]
        if session_id in self.processed_files:
            del self.processed_files[session_id]
    
    def get_active_sessions(self) -> List[str]:
        """Get list of active session IDs"""
        return list(self.chat_histories.keys())
