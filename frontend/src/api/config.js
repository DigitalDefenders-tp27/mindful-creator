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
  
  // Ensure endpoint doesn't have trailing slash
  endpoint = endpoint.endsWith('/') ? endpoint.slice(0, -1) : endpoint;
  
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
  // Remove trailing slash from API_URL if it exists
  const baseUrl = API_URL.endsWith('/') ? API_URL.slice(0, -1) : API_URL;
  
  // If endpoint already has /api prefix
  if (endpoint.startsWith('/api/')) {
    // Remove the leading slash to avoid double slashes
    const path = endpoint.startsWith('/') ? endpoint.substring(1) : endpoint;
    return `${baseUrl}/${path}`;
  }
  
  // If endpoint doesn't have /api prefix, add it
  const path = endpoint.startsWith('/') ? endpoint.substring(1) : endpoint;
  return `${baseUrl}/api/${path}`;
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
    // Don't send credentials by default to avoid CORS preflight issues
    credentials: options.credentials || 'omit',
  };
  
  // In development, don't use CORS mode (will be handled by the Vite proxy)
  if (!import.meta.env.DEV) {
    fetchOptions.mode = 'cors';
  }
  
  try {
    const response = await fetch(url, fetchOptions);
    
    // Handle HTTP redirects if needed
    if ([301, 302, 307, 308].includes(response.status)) {
      const redirectUrl = response.headers.get('Location');
      console.log(`Received redirect to: ${redirectUrl}`);
      
      // Ensure redirect URL uses HTTPS (except for localhost)
      const secureRedirectUrl = redirectUrl?.startsWith('http://')
        ? (redirectUrl.includes('localhost') ? redirectUrl : redirectUrl.replace('http://', 'https://'))
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
      // If we get a 500 error, include more details in the error message
      if (response.status === 500) {
        let errorDetails;
        try {
          // Try to parse the error response if possible
          errorDetails = await response.text();
          console.error('Server 500 error details:', errorDetails);
        } catch (textError) {
          errorDetails = 'No error details available';
        }
        throw new Error(`API request failed with status 500 - Server Error: ${errorDetails}`);
      }
      
      throw new Error(`API request failed with status ${response.status}`);
    }
    
    try {
      return await response.json();
    } catch (jsonError) {
      console.warn('Response was not JSON:', jsonError);
      return { success: true, message: 'Operation completed (no JSON response)' };
    }
  } catch (error) {
    console.error(`API Error (${endpoint}):`, error);
    throw error;
  }
} 