import React from 'react';
import { Sparkles, Settings } from 'lucide-react';

const Header = ({ showSettings, setShowSettings }) => {
  return (
    <div className="bg-white/80 backdrop-blur-lg rounded-2xl shadow-xl p-6 mb-6 border border-white">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="bg-gradient-to-br from-blue-500 to-purple-600 p-3 rounded-xl">
            <Sparkles className="w-8 h-8 text-white" />
          </div>
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              AI Assistant Pro
            </h1>
            <p className="text-gray-600 text-sm">Powered by Llama 3.3 70B</p>
          </div>
        </div>
        <button
          onClick={() => setShowSettings(!showSettings)}
          className="p-3 hover:bg-gray-100 rounded-xl transition-colors"
        >
          <Settings className="w-6 h-6 text-gray-600" />
        </button>
      </div>
    </div>
  );
};

export default Header;
