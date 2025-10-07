/**
 * API Client for AI Assistant Pro Backend
 */

const API_BASE_URL = 'http://localhost:8000';

/**
 * Upload PDF files to the backend
 */
export const uploadPDFs = async (files, sessionId) => {
  const formData = new FormData();
  
  files.forEach(file => {
    formData.append('files', file);
  });
  formData.append('session_id', sessionId);

  const response = await fetch(`${API_BASE_URL}/pdf/upload`, {
    method: 'POST',
    body: formData,
  });
  
  if (!response.ok) {
    throw new Error('Failed to upload PDFs');
  }
  
  return response.json();
};

/**
 * Send chat message to PDF chat endpoint
 */
export const sendChatMessage = async (query, sessionId, settings) => {
  const response = await fetch(`${API_BASE_URL}/pdf/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query,
      session_id: sessionId,
      temperature: settings.temperature,
      max_tokens: settings.maxTokens,
      search_k: settings.searchK
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to send chat message');
  }
  
  return response.json();
};

/**
 * Send search query to web search endpoint
 */
export const sendSearchQuery = async (query, sessionId, settings) => {
  const response = await fetch(`${API_BASE_URL}/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query,
      session_id: sessionId,
      temperature: settings.temperature,
      max_tokens: settings.maxTokens
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to perform search');
  }
  
  return response.json();
};

/**
 * Check backend health status
 */
export const checkHealth = async () => {
  const response = await fetch(`${API_BASE_URL}/health`);
  
  if (!response.ok) {
    throw new Error('Backend is not healthy');
  }
  
  return response.json();
};
