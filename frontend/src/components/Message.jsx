import React from 'react';

const Message = ({ message }) => {
  return (
    <div className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-3xl rounded-2xl p-4 ${
          message.role === 'user'
            ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white'
            : 'bg-gray-50 text-gray-800'
        }`}
      >
        <div className="whitespace-pre-wrap">{message.content}</div>
        {message.sources && message.sources.length > 0 && (
          <details className="mt-3 text-sm">
            <summary className="cursor-pointer font-medium opacity-80">
              📚 Sources ({message.sources.length})
            </summary>
            <div className="mt-2 space-y-2">
              {message.sources.map((src, i) => (
                <div key={i} className="text-xs opacity-70 border-l-2 border-white/30 pl-2">
                  {typeof src === 'string' ? (
                    src
                  ) : (
                    <>
                      <div className="font-semibold">{src.source}</div>
                      {src.page && <div>Page: {src.page}</div>}
                      {src.content && <div className="mt-1 italic">{src.content}</div>}
                    </>
                  )}
                </div>
              ))}
            </div>
          </details>
        )}
      </div>
    </div>
  );
};

export default Message;
