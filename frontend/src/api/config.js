// API configuration
const API_URL = import.meta.env.VITE_BACKEND_URL || 'https://api.tiezhu.org';

// Function to create API URLs with the correct base
export function getApiUrl(endpoint) {
  // If endpoint already starts with http, ensure it uses https
  if (endpoint.startsWith('http://')) {
    endpoint = endpoint.replace('http://', 'https://');
  }
  
  // If endpoint already starts with https, return as is (already absolute)
  if (endpoint.startsWith('https://')) {
    return endpoint;
  }
  
  // Development environment with Vite proxy
  if (import.meta.env.DEV) {
    // If endpoint already starts with /api/, return as is
    if (endpoint.startsWith('/api/')) {
      return endpoint;
    }
    
    // Add /api/ prefix if needed
    const path = endpoint.startsWith('/') ? endpoint.substring(1) : endpoint;
    return `/api/${path}`;
  }
  
  // Production environment
  // If endpoint already has /api prefix
  if (endpoint.startsWith('/api/')) {
    // Remove the leading slash to avoid double slashes
    const path = endpoint.startsWith('/') ? endpoint.substring(1) : endpoint;
    return `${API_URL}/${path}`;
  }
  
  // If endpoint doesn't have /api prefix, add it
  const path = endpoint.startsWith('/') ? endpoint.substring(1) : endpoint;
  return `${API_URL}/api/${path}`;
}

// Helper for fetch with proper error handling
export async function apiFetch(endpoint, options = {}) {
  const url = getApiUrl(endpoint);
  console.log(`API Request to: ${url}`);
  
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });
    
    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error(`API Error (${endpoint}):`, error);
    throw error;
  }
} 