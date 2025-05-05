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

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # 本地开发
        "https://mindful-creator.vercel.app",  # 主Vercel域名
        "https://mindful-creator-mcqbwi1f8-tp27.vercel.app",
        "https://tiezhu.org",
        "https://www.tiezhu.org"
    ],
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
)

from transformers import AutoTokenizer
import sys, os, time, json, torch

# === 模型 / tokenizer 路径 ===================================================
TOKENIZER_DIR = "/app/bert-base-uncased"   # Dockerfile 中已下载好 base BERT
MODEL_DIR     = "/app/nlp"                 # 克隆下来的 CommentResponse 空间
WEIGHTS_FILE  = os.path.join(MODEL_DIR, "pytorch_model.bin")
CFG_FILE      = os.path.join(MODEL_DIR, "config.json")

@app.on_event("startup")
async def load_nlp_model():
    """加载自定义 CommentMTLModel + tokenizer 并写入 app.state"""
    t0 = time.time()
    try:
        # 1) 校验所有关键路径
        for p in (TOKENIZER_DIR, MODEL_DIR, WEIGHTS_FILE, CFG_FILE):
            if not os.path.exists(p):
                raise FileNotFoundError(f"Missing file/dir: {p}")

        # 2) 加载 tokenizer（离线）
        logger.info(f"Tokenizer ← {TOKENIZER_DIR}")
        tokenizer = AutoTokenizer.from_pretrained(
            TOKENIZER_DIR,
            local_files_only=True
        )

        # 3) 动态导入自定义模型类
        if MODEL_DIR not in sys.path:
            sys.path.insert(0, MODEL_DIR)
        from model import CommentMTLModel  # noqa: E402

        # 4) 读取 config.json 并初始化模型，注意使用本地 BERT 目录作为 base
        with open(CFG_FILE, "r") as f:
            cfg = json.load(f)

        model = CommentMTLModel(
            model_name=TOKENIZER_DIR,                 # ← 指向本地 BERT
            num_sentiment_labels=cfg["num_sentiment_labels"],
            num_toxicity_labels=cfg["num_toxicity_labels"],
            dropout_prob=cfg.get("dropout_prob", 0.1)
        )

        # 5) 覆盖式加载 MTL head 的权重
        state_dict = torch.load(WEIGHTS_FILE, map_location="cpu")
        model.load_state_dict(state_dict)
        model.eval()

        # 6) 挂载到 app.state
        app.state.tokenizer    = tokenizer
        app.state.model        = model
        app.state.model_loaded = True
        logger.info(f"✅ NLP model ready ({time.time()-t0:.2f}s)")

    except Exception as exc:
        app.state.model_loaded     = False
        app.state.model_load_error = str(exc)
        logger.exception(f"❌ Failed to load NLP model: {exc}")

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


