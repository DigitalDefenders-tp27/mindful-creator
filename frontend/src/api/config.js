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
  
  // Set proper headers and handle redirects
  const fetchOptions = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      ...options.headers,
    },
    // Allow automatic redirects
    redirect: 'follow',
  };
  
  try {
    const response = await fetch(url, fetchOptions);
    
    // Check if we received a redirect
    if (response.status === 307 || response.status === 308) {
      const redirectUrl = response.headers.get('Location');
      console.log(`Received redirect to: ${redirectUrl}`);
      
      // Ensure redirect URL uses HTTPS
      const secureRedirectUrl = redirectUrl?.startsWith('http://')
        ? redirectUrl.replace('http://', 'https://')
        : redirectUrl;
        
      if (secureRedirectUrl) {
        // Follow the redirect manually with the same options
        console.log(`Following redirect to: ${secureRedirectUrl}`);
        const redirectResponse = await fetch(secureRedirectUrl, fetchOptions);
        
        if (!redirectResponse.ok) {
          throw new Error(`Redirect request failed with status ${redirectResponse.status}`);
        }
        
        return await redirectResponse.json();
      }
    }
    
    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error(`API Error (${endpoint}):`, error);
    throw error;
  }
} 