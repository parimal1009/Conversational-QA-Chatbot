import React from 'react';

const LoadingIndicator = () => {
  return (
    <div className="flex justify-start">
      <div className="bg-gray-50 rounded-2xl p-4">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
          <div 
            className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" 
            style={{animationDelay: '0.2s'}}
          ></div>
          <div 
            className="w-2 h-2 bg-pink-500 rounded-full animate-bounce" 
            style={{animationDelay: '0.4s'}}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default LoadingIndicator;
