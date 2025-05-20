# Backend Service Configuration Guide

## Standardised Backend Service

To ensure consistency and maintainability of the application, all frontend components should use a unified backend service address:

```
https://api.tiezhu.org
```

## Environment Variable Setup

Create a `frontend/.env.local` file (not committed to version control) and add the following configuration:

```
# Backend API base URL
VITE_BACKEND_URL=https://api.tiezhu.org

# WebSocket address (if applicable)
VITE_WEBSOCKET_URL=wss://api.tiezhu.org/ws
```

## Usage in Components

All components should reference the backend service as follows:

```javascript
// Correct approach: Use environment variables with api.tiezhu.org as fallback
const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || 'https://api.tiezhu.org';

// WebSocket connection
const WS_URL = import.meta.env.VITE_WEBSOCKET_URL || 'wss://api.tiezhu.org/ws';
```

## Avoid Direct References

Do not directly reference the following domains:
- ❌ `gleaming-celebration-production-66cb.up.railway.app`
- ❌ `mindful-creator-production.up.railway.app`
- ❌ Any other Railway.app or Vercel.app domains

These are infrastructure addresses for deployed services and may change. Use api.tiezhu.org as the unified entry point.

## CORS Configuration

The backend service has been configured to allow the following origins:
- `https://tiezhu.org`
- `https://www.tiezhu.org`
- `https://inflowence.org`
- `https://www.inflowence.org`
- Local servers for development

To add other domains, please modify the backend CORS configuration. 