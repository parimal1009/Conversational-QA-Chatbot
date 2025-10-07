# 🚀 AI Assistant Pro

A full-stack AI application combining **PDF Chat** and **Web Search** capabilities, powered by **Llama 3.3 70B** through Groq's ultra-fast inference API.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![React](https://img.shields.io/badge/React-18.2-61DAFB.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 📄 PDF Chat
- Upload and chat with multiple PDF documents
- Advanced context-aware responses with source citations
- Conversation history management
- Session-based document storage
- Page-level source references

### 🔍 Web Search
- Search across multiple sources simultaneously
- Web search via DuckDuckGo
- Academic papers via arXiv
- General knowledge via Wikipedia
- Intelligent source aggregation

### 🎨 Modern UI
- Beautiful white-themed interface with gradient animations
- Responsive design for all devices
- Real-time streaming responses
- Export chat history functionality
- Configurable LLM parameters

## 🏗️ Project Structure

```
ai-assistant-pro/
├── backend/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration settings
│   ├── models.py               # Pydantic models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── pdf_routes.py       # PDF chat endpoints
│   │   ├── search_routes.py    # Web search endpoints
│   │   └── system_routes.py    # System endpoints
│   └── services/
│       ├── __init__.py
│       ├── pdf_service.py      # PDF processing service
│       └── search_service.py   # Search service
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── SettingsPanel.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── ChatArea.jsx
│   │   │   ├── Message.jsx
│   │   │   └── LoadingIndicator.jsx
│   │   ├── utils/
│   │   │   └── api.js          # API client
│   │   ├── App.jsx             # Main React component
│   │   ├── main.jsx            # React entry point
│   │   └── index.css           # Global styles
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
├── .env                        # Environment variables
├── requirements.txt            # Python dependencies
├── .gitignore
└── README.md
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - High-performance Python API framework
- **LangChain** - LLM orchestration framework
- **Groq** - Ultra-fast LLM inference
- **FAISS** - Vector similarity search
- **HuggingFace** - Embeddings models
- **PyMuPDF** - PDF processing

### Frontend
- **React 18** - Modern UI framework
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first styling
- **Lucide React** - Beautiful icons

## 📋 Prerequisites

- **Python 3.9+**
- **Node.js 18+** and npm/yarn
- **Groq API Key** - [Get one here](https://console.groq.com/)
- **HuggingFace Token** (optional) - [Get one here](https://huggingface.co/settings/tokens)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
cd C:\Users\parim\Desktop\CBSE
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Your `.env` file is already configured with API keys.

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

### 4. Run the Application

**Terminal 1 - Backend:**
```bash
# Make sure you're in the root directory and venv is activated
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
# Navigate to frontend directory
cd frontend

# Start development server
npm run dev
```

**Access the application at:** http://localhost:3000

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Main Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/pdf/upload` | POST | Upload PDF documents |
| `/pdf/chat` | POST | Chat with uploaded PDFs |
| `/search` | POST | Search web, arXiv, and Wikipedia |
| `/session/{id}` | DELETE | Clear session data |
| `/sessions` | GET | List active sessions |
| `/health` | GET | Health check |

## 🎯 Usage

### PDF Chat Mode

1. Click **"PDF Chat"** mode
2. Click **"Upload PDFs"** and select your PDF files
3. Wait for processing confirmation
4. Ask questions about your documents
5. Get answers with source citations

**Example questions:**
- "Summarize the main points of this document"
- "What does the paper say about methodology?"
- "Compare the findings in sections 3 and 5"

### Web Search Mode

1. Click **"Web Search"** mode
2. Ask any question
3. Get answers from multiple sources

**Example questions:**
- "What are the latest developments in AI?"
- "Explain quantum computing simply"
- "Latest research on climate change"

## ⚙️ Configuration

### LLM Settings (Adjustable in UI)

- **Temperature** (0.0 - 1.0)
  - `0.0-0.3`: Precise, deterministic answers
  - `0.4-0.7`: Balanced creativity and accuracy
  - `0.8-1.0`: More creative responses

- **Max Tokens** (100 - 4096)
  - Controls response length
  - Default: 2048

- **Search K** (1 - 10, PDF Chat only)
  - Number of document chunks to retrieve
  - Default: 4

### Backend Configuration

Edit `backend/config.py` to customize:
- Model name
- Chunk size and overlap
- Search parameters
- CORS settings

## 🐛 Troubleshooting

### Backend Issues

**Module not found errors:**
```bash
pip install --upgrade -r requirements.txt
```

**API key errors:**
- Verify `.env` file has correct API keys
- Check that keys are not expired
- Ensure no extra spaces in `.env`

**Port already in use:**
```bash
# Use a different port
uvicorn backend.main:app --reload --port 8001
```

### Frontend Issues

**Cannot connect to backend:**
- Ensure backend is running on port 8000
- Check CORS settings in `backend/config.py`
- Verify `API_BASE_URL` in `frontend/src/utils/api.js`

**Build errors:**
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 🚀 Production Deployment

### Backend

**Using Docker:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Deploy to:**
- Railway
- Render
- Heroku
- AWS Lambda (with Mangum)

### Frontend

```bash
cd frontend
npm run build
```

Deploy `dist/` folder to:
- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront

## 📊 Performance Tips

- Use MMR search for diverse document chunks
- Adjust chunk size based on document type
- Enable LangChain tracing for debugging
- Use FAISS GPU for large document collections
- Implement caching for frequent queries

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🙏 Acknowledgments

- **Groq** for ultra-fast LLM inference
- **LangChain** for the amazing orchestration framework
- **HuggingFace** for embeddings models
- **Meta** for Llama 3.3 70B model

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review API documentation

## 🔮 Future Roadmap

- [ ] Support for more document types (DOCX, TXT, etc.)
- [ ] Voice input/output
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Team collaboration features
- [ ] Document comparison tools
- [ ] API rate limiting
- [ ] Redis caching layer

---

**Built with ❤️ using React, FastAPI, and Groq**
