# 🚀 Quick Setup Guide - AI Assistant Pro

This guide will help you get the AI Assistant Pro up and running in minutes.

## ✅ Prerequisites Check

Before starting, make sure you have:
- [ ] Python 3.9 or higher installed
- [ ] Node.js 18 or higher installed
- [ ] Your Groq API key (already in `.env`)
- [ ] Your HuggingFace token (already in `.env`)

## 📦 Installation

### Option 1: Quick Start (Windows)

Simply run the provided batch scripts:

**Terminal 1 - Backend:**
```batch
run_backend.bat
```

**Terminal 2 - Frontend:**
```batch
run_frontend.bat
```

The scripts will automatically:
- Create virtual environment (if needed)
- Install all dependencies
- Start the servers

### Option 2: Manual Setup

#### Backend Setup

1. **Create and activate virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Verify .env file:**
Your `.env` file should contain:
```env
GROQ_API_KEY=gsk_...
HF_TOKEN=hf_...
```

4. **Start backend server:**
```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install Node dependencies:**
```bash
npm install
```

3. **Start development server:**
```bash
npm run dev
```

## 🌐 Access the Application

Once both servers are running:

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc

## 🧪 Test the Setup

### Test Backend

1. Open http://localhost:8000/health in your browser
2. You should see: `{"status":"healthy","model":"llama-3.3-70b-versatile","timestamp":"..."}`

### Test Frontend

1. Open http://localhost:3000
2. You should see the AI Assistant Pro interface
3. Try switching between PDF Chat and Web Search modes

## 📄 First PDF Chat

1. Click **"PDF Chat"** mode
2. Click **"Upload PDFs"** button
3. Select a PDF file from your computer
4. Wait for "Successfully processed" message
5. Ask a question like: "Summarize this document"

## 🔍 First Web Search

1. Click **"Web Search"** mode
2. Type a question like: "What is machine learning?"
3. Press Enter or click Send
4. Wait for the AI response with sources

## ⚙️ Adjust Settings

Click the **Settings** icon (⚙️) in the header to adjust:
- **Temperature:** Controls response creativity (0.0-1.0)
- **Max Tokens:** Maximum response length (100-4096)
- **Search K:** Number of document chunks to retrieve (1-10)

## 🐛 Common Issues

### Backend won't start

**Error:** `ModuleNotFoundError`
```bash
# Solution: Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**Error:** `Port 8000 already in use`
```bash
# Solution: Use different port
uvicorn backend.main:app --reload --port 8001
```

### Frontend won't start

**Error:** `Cannot find module`
```bash
# Solution: Reinstall dependencies
cd frontend
rm -rf node_modules
npm install
```

**Error:** `EADDRINUSE: address already in use`
```bash
# Solution: Port 3000 is busy, Vite will prompt to use another port
# Just press 'y' when prompted
```

### Can't connect to backend

**Check:** Backend is running on port 8000
**Check:** No firewall blocking localhost
**Fix:** Update `API_BASE_URL` in `frontend/src/utils/api.js` if needed

### API Key errors

**Check:** `.env` file exists in root directory
**Check:** API keys have no extra spaces or quotes
**Check:** Groq API key is valid at https://console.groq.com/

## 📝 Project Structure Verification

Your project should look like this:

```
CBSE/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── pdf_routes.py
│   │   ├── search_routes.py
│   │   └── system_routes.py
│   └── services/
│       ├── __init__.py
│       ├── pdf_service.py
│       └── search_service.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── utils/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── .env
├── requirements.txt
├── README.md
├── run_backend.bat
└── run_frontend.bat
```

## 🎉 Next Steps

Now that everything is set up:

1. **Read the README.md** for detailed feature documentation
2. **Explore the API** at http://localhost:8000/docs
3. **Try PDF Chat** with your documents
4. **Test Web Search** with various queries
5. **Adjust settings** to optimize responses
6. **Export chats** to save your conversations

## 💡 Tips

- **PDF Chat works best with** technical documents, research papers, reports
- **Use Temperature 0.1-0.3** for factual questions
- **Use Temperature 0.7-0.9** for creative content
- **Increase Search K** for more context in answers
- **Web Search** can access current information

## 🆘 Need Help?

- Check the **README.md** for detailed documentation
- Visit API docs at http://localhost:8000/docs
- Review troubleshooting section in README
- Check your terminal for error messages

---

**Happy coding! 🚀**
