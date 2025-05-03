import os
import logging
import time
import sys
import traceback
import importlib
import psutil  # 新增用于监控系统资源
from typing import Dict, Any, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
import datetime
import uvicorn
import platform

from app.api.router import router as api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
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
    logger.warning("Extra routes skipped: %s: %s", type(e).__name__, e)

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

# 记录启动时间
start_time = time.time()
logger.info(f"====== MINDFUL CREATOR BACKEND STARTING ======")
logger.info(f"Python version: {platform.python_version()}")
logger.info(f"Platform: {platform.platform()}")

# 记录系统资源状态
def log_system_resources():
    """记录系统资源使用情况"""
    try:
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        logger.info(f"Memory Usage: RSS={memory_info.rss / 1024 / 1024:.2f}MB, VMS={memory_info.vms / 1024 / 1024:.2f}MB")
        
        cpu_percent = process.cpu_percent(interval=0.1)
        logger.info(f"CPU Usage: {cpu_percent:.2f}%")
        
        # 系统内存情况
        virtual_memory = psutil.virtual_memory()
        logger.info(f"System Memory: Total={virtual_memory.total / 1024 / 1024 / 1024:.2f}GB, "
                   f"Available={virtual_memory.available / 1024 / 1024 / 1024:.2f}GB, "
                   f"Used={virtual_memory.percent:.2f}%")
    except Exception as e:
        logger.warning(f"Failed to log system resources: {e}")

# 记录启动资源状态
log_system_resources()

# 记录模型状态
model_loaded = os.environ.get("MODEL_LOADED", "false").lower() == "true"
logger.info(f"MODEL_LOADED environment variable: {os.environ.get('MODEL_LOADED', 'not set')}")
logger.info(f"Model loaded status: {model_loaded}")

# 尝试加载各个路由模块
ROUTES = [
    "app.api.router",
    "app.api.youtube.routes",
]

logger.info("Loading API routes...")
for route_module in ROUTES:
    try:
        module_start_time = time.time()
        logger.info(f"Loading route module: {route_module}")
        module = importlib.import_module(route_module)
        
        # 如果模块有路由器属性，则包含它
        if hasattr(module, "router"):
            logger.info(f"Including router from {route_module}")
            api_router.include_router(module.router)
        
        logger.info(f"Loaded {route_module} in {time.time() - module_start_time:.2f} seconds")
    except Exception as e:
        logger.error(f"Failed to load {route_module}: {e}")
        logger.error(traceback.format_exc())

# 记录应用启动完成
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
