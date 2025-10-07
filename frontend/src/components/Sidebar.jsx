import React from 'react';
import { Sparkles, FileText, Search, Upload, Trash2, Download } from 'lucide-react';

const Sidebar = ({ 
  activeTab, 
  setActiveTab, 
  uploadedFiles, 
  fileInputRef, 
  handleFileUpload,
  clearChat,
  exportChat 
}) => {
  return (
    <div className="lg:col-span-1 space-y-4">
      {/* Mode Selector */}
      <div className="bg-white/80 backdrop-blur-lg rounded-2xl shadow-xl p-4 border border-white">
        <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-purple-500" />
          Mode
        </h3>
        <div className="space-y-2">
          <button
            onClick={() => setActiveTab('chat')}
            className={`w-full p-3 rounded-xl flex items-center gap-3 transition-all ${
              activeTab === 'chat'
                ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg'
                : 'bg-gray-50 text-gray-700 hover:bg-gray-100'
            }`}
          >
            <FileText className="w-5 h-5" />
            <span className="font-medium">PDF Chat</span>
          </button>
          <button
            onClick={() => setActiveTab('search')}
            className={`w-full p-3 rounded-xl flex items-center gap-3 transition-all ${
              activeTab === 'search'
                ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg'
                : 'bg-gray-50 text-gray-700 hover:bg-gray-100'
            }`}
          >
            <Search className="w-5 h-5" />
            <span className="font-medium">Web Search</span>
          </button>
        </div>
      </div>

      {/* File Upload */}
      {activeTab === 'chat' && (
        <div className="bg-white/80 backdrop-blur-lg rounded-2xl shadow-xl p-4 border border-white">
          <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
            <Upload className="w-5 h-5 text-blue-500" />
            Documents
          </h3>
          <input
            ref={fileInputRef}
            type="file"
            multiple
            accept=".pdf"
            onChange={handleFileUpload}
            className="hidden"
          />
          <button
            onClick={() => fileInputRef.current?.click()}
            className="w-full p-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl hover:shadow-lg transition-all flex items-center justify-center gap-2"
          >
            <Upload className="w-4 h-4" />
            Upload PDFs
          </button>
          
          {uploadedFiles.length > 0 && (
            <div className="mt-3 space-y-2">
              {uploadedFiles.map((file, idx) => (
                <div key={idx} className="text-xs text-gray-600 bg-gray-50 p-2 rounded-lg">
                  📄 {file}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Actions */}
      <div className="bg-white/80 backdrop-blur-lg rounded-2xl shadow-xl p-4 border border-white space-y-2">
        <button
          onClick={clearChat}
          className="w-full p-3 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 transition-colors flex items-center justify-center gap-2"
        >
          <Trash2 className="w-4 h-4" />
          Clear Chat
        </button>
        <button
          onClick={exportChat}
          className="w-full p-3 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 transition-colors flex items-center justify-center gap-2"
        >
          <Download className="w-4 h-4" />
          Export
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
