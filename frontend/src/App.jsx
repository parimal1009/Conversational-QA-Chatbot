import React, { useState, useRef, useEffect } from 'react';
import Header from './components/Header';
import SettingsPanel from './components/SettingsPanel';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';
import { uploadPDFs, sendChatMessage, sendSearchQuery } from './utils/api';

function App() {
  const [activeTab, setActiveTab] = useState('chat');
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [sessionId, setSessionId] = useState(`session_${Date.now()}`);
  const [showSettings, setShowSettings] = useState(false);
  const [settings, setSettings] = useState({
    temperature: 0.3,
    maxTokens: 2048,
    searchK: 4
  });
  
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const handleFileUpload = async (e) => {
    const files = Array.from(e.target.files);
    if (files.length === 0) return;

    setLoading(true);
    try {
      const data = await uploadPDFs(files, sessionId);
      setUploadedFiles(prev => [...prev, ...data.processed_files]);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `✅ ${data.message}`
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `❌ Error uploading files: ${error.message}`
      }]);
    } finally {
      setLoading(false);
      e.target.value = '';
    }
  };

  const handleSendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      let data;
      if (activeTab === 'chat') {
        data = await sendChatMessage(input, sessionId, settings);
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: data.answer,
          sources: data.sources
        }]);
      } else {
        data = await sendSearchQuery(input, sessionId, settings);
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: data.response,
          sources: data.sources
        }]);
      }
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `❌ Error: ${error.message}`
      }]);
    } finally {
      setLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
    setSessionId(`session_${Date.now()}`);
    setUploadedFiles([]);
  };

  const exportChat = () => {
    const chatText = messages.map(m => `${m.role.toUpperCase()}: ${m.content}`).join('\n\n');
    const blob = new Blob([chatText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `chat_${sessionId}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob"></div>
        <div className="absolute top-40 right-10 w-72 h-72 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-1/2 w-72 h-72 bg-pink-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-4000"></div>
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 py-6">
        <Header showSettings={showSettings} setShowSettings={setShowSettings} />
        
        <SettingsPanel 
          settings={settings} 
          setSettings={setSettings} 
          showSettings={showSettings} 
        />

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          <Sidebar
            activeTab={activeTab}
            setActiveTab={setActiveTab}
            uploadedFiles={uploadedFiles}
            fileInputRef={fileInputRef}
            handleFileUpload={handleFileUpload}
            clearChat={clearChat}
            exportChat={exportChat}
          />
          
          <ChatArea
            activeTab={activeTab}
            messages={messages}
            loading={loading}
            input={input}
            setInput={setInput}
            handleSendMessage={handleSendMessage}
            messagesEndRef={messagesEndRef}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
