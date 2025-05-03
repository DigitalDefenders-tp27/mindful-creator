import os
import logging
import time
from typing import Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import datetime
import uvicorn

from app.api.router import router as api_router
from app.api.relaxation.routes import router as relaxation_router
from app.api.notes.routes import router as notes_router
from app.api.youtube.routes import router as youtube_router
from app.database import get_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Mindful Creator API",
    description="API for analyzing YouTube comments and providing response strategies",
    version="1.0.0"
)

# Setup CORS
origins = [
    "http://localhost:3000", 
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "https://mindful-creator-git-main-tiezhu.vercel.app",
    "https://mindful-creator.vercel.app",
    "https://mindful-creator-tiezhu.vercel.app",
    "https://mindful-creator-production-e20c.up.railway.app",
    "https://gleaming-celebration-production-0ae0.up.railway.app",
    "*"  # Allow all origins as fallback - make sure this is at the end
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://(.*\.)?mindful-creator.*\.vercel\.app|https://.*\.up\.railway\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=86400,  # Cache preflight requests for 24 hours
    expose_headers=["Content-Type", "X-API-Version"]
)

# Critical healthcheck endpoints - must be added before any other route registration
# This ensures the endpoints are available even if other parts of the app fail to initialize

@app.get("/")
def root() -> Dict[str, str]:
    """Root path simplified health check - always responds for Railway's healthcheck"""
    logger.info("Root endpoint called - responding with basic status")
    return {"status": "online"}

@app.get("/health")
def health_check() -> Dict[str, Any]:
    """Simple health check endpoint for monitoring application status"""
    logger.info("Health check endpoint called")
    try:
        # Ensure we have valid data in the response
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "environment": os.environ.get("APP_ENV", "development"),
            "nlp_model_loaded": os.environ.get("MODEL_LOADED", "false").lower() == "true",
            "api_version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        # Still return a valid response even if there's an error
        return {
            "status": "degraded",
            "error": str(e),
            "timestamp": time.time()
        }

# Register routes - moved after health check endpoint
logger.info("Registering API routes")
app.include_router(api_router, prefix="/api")
app.include_router(relaxation_router, prefix="/api/relaxation")
app.include_router(notes_router, prefix="/api/notes")
app.include_router(youtube_router, prefix="/api/youtube")

# Add WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    client_id = id(websocket)
    logger.info(f"WebSocket connection attempt from client {client_id}")
    
    # Accept the connection without any validation
    await websocket.accept()
    logger.info(f"WebSocket connection accepted for client {client_id}")
    
    try:
        while True:
            # Wait for text messages from the client
            data = await websocket.receive_text()
            logger.info(f"Received message from client {client_id}: {data}")
            
            # Echo the message back to the client
            response = f"Echo: {data}"
            await websocket.send_text(response)
            logger.info(f"Sent response to client {client_id}: {response}")
    
    except WebSocketDisconnect:
        logger.info(f"Client {client_id} disconnected normally")
    except Exception as e:
        logger.error(f"Error in WebSocket connection with client {client_id}: {str(e)}")
    finally:
        logger.info(f"WebSocket connection with client {client_id} closed")

# WebSocket test endpoint for connection verification
@app.get("/ws-test")
async def websocket_test():
    """Simple endpoint to test if the server is capable of WebSocket connections"""
    return {"status": "ok", "message": "WebSocket test endpoint available"}

# Request processing middleware, add performance monitoring
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    
    # Record request information
    logger.info(f"Request: {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    # Add processing time header
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"Response time: {process_time:.2f}s")
    
    return response

if __name__ == "__main__":
    # Get port from environment with fallback
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting server on port {port}")
    logger.info(f"Environment: {os.environ.get('APP_ENV', 'development')}")
    logger.info(f"NLP model loaded: {os.environ.get('MODEL_LOADED', 'false').lower() == 'true'}")
    
    # Use optimized Uvicorn configuration
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        workers=1,  # Adjust worker count based on resources
        timeout_keep_alive=65
    ) 
