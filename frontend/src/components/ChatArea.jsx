import React from 'react';
import { MessageSquare, Send } from 'lucide-react';
import Message from './Message';
import LoadingIndicator from './LoadingIndicator';

const ChatArea = ({ 
  activeTab,
  messages, 
  loading, 
  input, 
  setInput, 
  handleSendMessage,
  messagesEndRef 
}) => {
  return (
    <div className="lg:col-span-3">
      <div className="bg-white/80 backdrop-blur-lg rounded-2xl shadow-xl border border-white flex flex-col h-[calc(100vh-220px)]">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.length === 0 && (
            <div className="text-center py-12">
              <div className="inline-block p-4 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full mb-4">
                <MessageSquare className="w-12 h-12 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">
                {activeTab === 'chat' ? 'Upload PDFs to Start' : 'Ask Me Anything'}
              </h3>
              <p className="text-gray-600">
                {activeTab === 'chat'
                  ? 'Upload PDF documents and chat with them using AI'
                  : 'Search the web, academic papers, and Wikipedia'}
              </p>
            </div>
          )}

          {messages.map((msg, idx) => (
            <Message key={idx} message={msg} />
          ))}
          
          {loading && <LoadingIndicator />}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="p-4 border-t border-gray-200">
          <div className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder={`Ask about ${activeTab === 'chat' ? 'your documents' : 'anything'}...`}
              className="flex-1 px-4 py-3 bg-gray-50 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-blue-500 transition-colors"
              disabled={loading}
            />
            <button
              onClick={handleSendMessage}
              disabled={loading || !input.trim()}
              className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatArea;
