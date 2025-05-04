import os
import logging
import time
import sys
import traceback
import importlib
import psutil  # Added for system resource monitoring
from typing import Dict, Any, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
import datetime
import uvicorn
import platform

# First import only the base router to ensure health check endpoint is available
from app.api.router import router as api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Record startup time
start_time = time.time()
logger.info(f"====== MINDFUL CREATOR BACKEND STARTING ======")
logger.info(f"Python version: {platform.python_version()}")
logger.info(f"Platform: {platform.platform()}")

# Record system resource status
def log_system_resources():
    """Log system resource usage"""
    try:
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        logger.info(f"Memory Usage: RSS={memory_info.rss / 1024 / 1024:.2f}MB, VMS={memory_info.vms / 1024 / 1024:.2f}MB")
        
        cpu_percent = process.cpu_percent(interval=0.1)
        logger.info(f"CPU Usage: {cpu_percent:.2f}%")
        
        # System memory information
        virtual_memory = psutil.virtual_memory()
        logger.info(f"System Memory: Total={virtual_memory.total / 1024 / 1024 / 1024:.2f}GB, "
                   f"Available={virtual_memory.available / 1024 / 1024 / 1024:.2f}GB, "
                   f"Used={virtual_memory.percent:.2f}%")
    except Exception as e:
        logger.warning(f"Failed to log system resources: {e}")

# Record startup resource status
log_system_resources()

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

# First register the API router which contains the health check endpoint
logger.info("Registering API router (contains health check endpoint)")
app.include_router(api_router, prefix="/api")

# Root endpoint for basic health check
@app.get("/")
def root() -> Dict[str, str]:
    """Root path simplified health check"""
    return {"status": "online"}

# Record model status
model_loaded = os.environ.get("MODEL_LOADED", "false").lower() == "true"
logger.info(f"MODEL_LOADED environment variable: {os.environ.get('MODEL_LOADED', 'not set')}")
logger.info(f"Model loaded status: {model_loaded}")

# Try to load other routes, even if it fails, health check endpoint won't be affected
ADDITIONAL_ROUTES = [
    ("app.api.relaxation.routes", "/api/relaxation"),
    ("app.api.notes.routes", "/api/notes"),
    ("app.api.youtube.routes", "/api/youtube")
]

logger.info("Loading additional routes...")
for route_module, prefix in ADDITIONAL_ROUTES:
    try:
        module_start_time = time.time()
        logger.info(f"Loading route module: {route_module}")
        module = importlib.import_module(route_module)
        
        # If the module has a router attribute, include it
        if hasattr(module, "router"):
            logger.info(f"Including router from {route_module} at prefix {prefix}")
            app.include_router(module.router, prefix=prefix)
            logger.info(f"Successfully loaded {route_module} in {time.time() - module_start_time:.2f} seconds")
        else:
            logger.warning(f"Module {route_module} does not have a router attribute")
    except Exception as e:
        logger.error(f"Failed to load {route_module}: {str(e)}")
        logger.error(traceback.format_exc())
        logger.info(f"Continuing startup despite failure to load {route_module}")

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
    method = request.method
    url = request.url.path
    
    logger.info(f"Request started: {method} {url}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        status_code = response.status_code
        logger.info(f"Request completed: {method} {url} - Status: {status_code} - Time: {process_time:.4f}s")
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Request failed: {method} {url} - Error: {str(e)} - Time: {process_time:.4f}s")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error", "error": str(e)}
        )

# Record application startup completion
startup_time = time.time() - start_time
logger.info(f"====== MINDFUL CREATOR BACKEND STARTED in {startup_time:.2f} seconds ======")
logger.info(f"API available at http://0.0.0.0:{os.environ.get('PORT', '8000')}")
log_system_resources()

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
