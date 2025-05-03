import os
import logging
import time
from typing import Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import datetime
import uvicorn

from app.api.router import router as api_router

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

# Setup CORS - Simplified to ensure it works in all environments
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=86400,  # Cache preflight requests for 24 hours
    expose_headers=["Content-Type", "X-API-Version"]
)

# First register the API router which contains the health check endpoint for Railway
logger.info("Registering API router (contains health check endpoint)")
app.include_router(api_router, prefix="/api")

# Root endpoint for basic health check
@app.get("/")
def root() -> Dict[str, str]:
    """Root path simplified health check"""
    return {"status": "online"}

# Load other routes conditionally
try:
    logger.info("Attempting to load additional routes")
    # Import other routers only after API router is registered
    from app.api.relaxation.routes import router as relaxation_router
    from app.api.notes.routes import router as notes_router
    from app.api.youtube.routes import router as youtube_router
    
    # Register additional routes
    app.include_router(relaxation_router, prefix="/api/relaxation")
    app.include_router(notes_router, prefix="/api/notes")
    app.include_router(youtube_router, prefix="/api/youtube")
    logger.info("Successfully loaded all additional routes")
except Exception as e:
    logger.error(f"Error loading additional routes: {str(e)}")
    logger.info("Continuing startup with basic functionality")

# Custom middleware to manually add CORS headers for all responses
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    
    # Add CORS headers to every response
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    
    return response

# Request processing middleware
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
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting server on port {port}")
    
    # Use optimized Uvicorn configuration
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        workers=1,
        timeout_keep_alive=65
    ) 
