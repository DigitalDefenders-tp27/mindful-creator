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

from transformers import AutoTokenizer, AutoModel
import pathlib, os.path

# 修改模型路径定义，确保它是绝对路径并且可检查存在性
MODEL_PATH = "/app/nlp"   # Dockerfile 克隆到的目录
FALLBACK_MODEL = "bert-base-uncased"  # 备用模型名称

@app.on_event("startup")
async def load_nlp_model():
    """一次性加载 tokenizer / model 并存到 app.state"""
    start = time.time()
    try:
        # 检查模型路径是否存在
        if not os.path.exists(MODEL_PATH):
            logger.warning(f"⚠️ NLP model path not found: {MODEL_PATH}")
            # 尝试列出/app目录内容以便调试
            try:
                app_contents = os.listdir("/app")
                logger.info(f"Contents of /app directory: {app_contents}")
            except Exception as dir_err:
                logger.warning(f"Could not list /app directory: {dir_err}")
                
            app.state.model_loaded = False
            app.state.model_load_error = f"Model path not found: {MODEL_PATH}"
            return
            
        logger.info(f"Loading NLP model from: {MODEL_PATH}")
        
        try:
            # 尝试加载本地模型
            tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
            model = AutoModel.from_pretrained(MODEL_PATH)
            app.state.tokenizer = tokenizer
            app.state.model = model
            app.state.model_loaded = True
            logger.info(f"NLP model loaded from local path ✅  ({time.time()-start:.2f}s)")
        except Exception as local_err:
            logger.warning(f"Failed to load model from local path: {local_err}")
            logger.info(f"Attempting to load fallback model: {FALLBACK_MODEL}")
            
            # 尝试加载备用模型
            try:
                tokenizer = AutoTokenizer.from_pretrained(FALLBACK_MODEL)
                model = AutoModel.from_pretrained(FALLBACK_MODEL)
                app.state.tokenizer = tokenizer
                app.state.model = model
                app.state.model_loaded = True
                app.state.using_fallback = True
                logger.info(f"Fallback NLP model loaded ✅  ({time.time()-start:.2f}s)")
            except Exception as fallback_err:
                # 如果备用模型也加载失败，使用空模型
                logger.error(f"Failed to load fallback model: {fallback_err}")
                app.state.model_loaded = False
                app.state.model_load_error = f"Failed to load both local and fallback models"
                app.state.using_placeholder = True
                logger.warning("Using placeholder NLP handling")
    except Exception as e:
        app.state.model_loaded = False
        app.state.model_load_error = str(e)
        logger.exception(f"❌ Failed to load NLP model: {e}")
        # 记录更多系统信息以便调试
        logger.error(f"Python path: {sys.path}")
        logger.error(f"Current working directory: {os.getcwd()}")

# Setup CORS - Updated to fix allow_credentials and allow_origins conflict
app.add_middleware(
    CORSMiddleware,
    # List of allowed origins
    allow_origins=[
        "https://mindful-creator.vercel.app",
        "https://www.tiezhu.org",
        "https://api.tiezhu.org",
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ],
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

# Additional health check endpoint at the root level for Railway
@app.get("/health")
async def root_health_check() -> Dict[str, Any]:
    """Root health check specifically for Railway"""
    logger.info("ROOT HEALTH CHECK ENDPOINT ACCESSED - Railway health check")
    return {"status": "healthy", "timestamp": datetime.datetime.now().isoformat(), "message": "Health check OK"}

# Explicit API health check endpoint to match railway.toml configuration
@app.get("/api/health")
async def api_health_check() -> Dict[str, Any]:
    """API health check endpoint for Railway deployment"""
    logger.info("API HEALTH CHECK ENDPOINT ACCESSED")
    return {"status": "healthy", "timestamp": datetime.datetime.now().isoformat(), "message": "Health check OK"}

# 添加诊断端点
@app.get("/api/diagnostics/nlp")
async def nlp_diagnostics() -> Dict[str, Any]:
    """诊断端点，用于检查NLP模型状态"""
    logger.info("NLP DIAGNOSTICS ENDPOINT ACCESSED")
    
    # 检查模型路径
    model_path_exists = os.path.exists(MODEL_PATH)
    
    # 列出目录内容
    app_contents = []
    nlp_contents = []
    try:
        app_contents = os.listdir("/app")
        if model_path_exists:
            nlp_contents = os.listdir(MODEL_PATH)
    except Exception as e:
        logger.error(f"Failed to list directories: {e}")
    
    # 收集诊断信息
    diagnostics = {
        "timestamp": datetime.datetime.now().isoformat(),
        "model_path": MODEL_PATH,
        "model_path_exists": model_path_exists,
        "model_loaded": getattr(app.state, "model_loaded", False),
        "model_load_error": getattr(app.state, "model_load_error", None),
        "app_directory_contents": app_contents,
        "nlp_directory_contents": nlp_contents,
        "environment": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "working_directory": os.getcwd()
        }
    }
    
    return diagnostics

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
# Use PORT environment variable for consistency with railway_startup.sh
port = int(os.environ.get("PORT", 8000))
logger.info(f"API available at http://0.0.0.0:{port}")
log_system_resources()

if __name__ == "__main__":
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


