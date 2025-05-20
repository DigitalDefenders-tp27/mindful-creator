import os
import logging
import time
import sys
import traceback
import importlib
import psutil  # Added for system resource monitoring
from typing import Dict, Any, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Request, Response, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, StreamingResponse
from fastapi.routing import APIRouter
import datetime
import uvicorn
import platform
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import affirmations, breaths, journals, memes, ratings

# Explicitly import the games router
from app.api.games import router as games_api_router # Assuming games_router is exported as router in app/api/games/__init__.py
from app.api.games.routes import router as game_router
from app.api.games.memory_match import router as memory_match_router
from app.api.games.memory_match import GameInitRequest # Ensure this import is present
import httpx
from starlette.responses import RedirectResponse

# First import only the base router to ensure health check endpoint is available
# from app.api.router import router as api_router
from app.api.youtube.routes import router as youtube_router

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

# Configure CORS middleware
# Define allowed origins for specific domains
allowed_origins = [
    "http://localhost:3000",  # Local development (frontend)
    "http://localhost:5173",  # Vite dev server (frontend)
    "https://mindful-creator.vercel.app",  # Main Vercel production domain
    "https://tiezhu.org", # Custom domain
    "https://www.tiezhu.org", # Custom domain with www
    "https://www.inflowence.org", # Inflowence domain
    "https://inflowence.org", # Inflowence domain without www
    # Add any other specific production/staging domains here
    "*", # Allow all origins temporarily for debugging
]

# Define a regex for Vercel preview deployments under your specific project/scope
# This matches URLs like: https://mindful-creator-<hash>-tp27.vercel.app
vercel_preview_regex = r"^https://mindful-creator-[a-zA-Z0-9\-]+-tp27\.vercel\.app$"

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins, # List of specific origins
    allow_origin_regex=vercel_preview_regex, # Regex for Vercel previews
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Explicitly specify allowed methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Add this to expose all response headers
    max_age=3600,  # Add cache time to improve performance
)

from transformers import AutoTokenizer
import sys, os, time, json, torch

# === Model / tokenizer paths ===================================================
TOKENIZER_DIR = "/app/bert-base-uncased"   # Base BERT already downloaded in Dockerfile
MODEL_DIR     = "/app/nlp"                 # Cloned CommentResponse space
WEIGHTS_FILE  = os.path.join(MODEL_DIR, "pytorch_model.bin")
CFG_FILE      = os.path.join(MODEL_DIR, "config.json")

@app.on_event("startup")
async def load_nlp_model():
    """Load custom CommentMTLModel + tokenizer and save to app.state"""
    t0 = time.time()
    try:
        # 1) Verify all key paths
        for p in (TOKENIZER_DIR, MODEL_DIR, WEIGHTS_FILE, CFG_FILE):
            if not os.path.exists(p):
                raise FileNotFoundError(f"Missing file/dir: {p}")

        # 2) Load tokenizer (offline)
        logger.info(f"Tokenizer ← {TOKENIZER_DIR}")
        tokenizer = AutoTokenizer.from_pretrained(
            TOKENIZER_DIR,
            local_files_only=True
        )

        # 3) Dynamically import custom model class
        if MODEL_DIR not in sys.path:
            sys.path.insert(0, MODEL_DIR)
        from model import CommentMTLModel  # noqa: E402

        # 4) Read config.json and initialize model, note use of local BERT directory as base
        with open(CFG_FILE, "r") as f:
            cfg = json.load(f)

        model = CommentMTLModel(
            model_name=TOKENIZER_DIR,                 # ← Points to local BERT
            num_sentiment_labels=cfg["num_sentiment_labels"],
            num_toxicity_labels=cfg["num_toxicity_labels"],
            dropout_prob=cfg.get("dropout_prob", 0.1)
        )

        # 5) Load MTL head weights
        state_dict = torch.load(WEIGHTS_FILE, map_location="cpu")
        model.load_state_dict(state_dict, strict=False)
        model.eval()

        # 6) Mount to app.state
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
app.include_router(youtube_router, prefix="/api")

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

# Add diagnostics endpoint
@app.get("/api/diagnostics/nlp")
async def nlp_diagnostics() -> Dict[str, Any]:
    """Diagnostics endpoint for checking NLP model status"""
    logger.info("NLP DIAGNOSTICS ENDPOINT ACCESSED")
    
    # Check model path
    model_path_exists = os.path.exists(MODEL_PATH)
    
    # List directory contents
    app_contents = []
    nlp_contents = []
    try:
        app_contents = os.listdir("/app")
        if model_path_exists:
            nlp_contents = os.listdir(MODEL_PATH)
    except Exception as e:
        logger.error(f"Failed to list directories: {e}")
    
    # Collect diagnostic information
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
    ("app.api.youtube.routes", "/api/youtube"),
    ("app.api.copyright.routes", "/api/copyright"),
    ("app.routers.affirmations", "/api/affirmations"),
    ("app.routers.breaths", "/api/breaths"),
    ("app.routers.journals", "/api/journals"),
    ("app.routers.memes", "/api/memes"),
    ("app.routers.ratings", "/api/ratings")
    # ("app.api.games", "/api/games") # Removed from dynamic list
]

# Explicitly include the games router
app.include_router(games_api_router, prefix="/api/games")
logger.info("Explicitly included games_api_router at prefix /api/games")

# Explicitly include the ratings router
app.include_router(ratings.router, prefix="/api/ratings")
logger.info("Explicitly included ratings router at prefix /api/ratings")

# Explicitly include the game router
app.include_router(game_router, prefix="/api/games")
logger.info("Explicitly included game router at prefix /api/games")

# Explicitly include the memory match router
app.include_router(memory_match_router, prefix="/api/games/memory_match")
logger.info("Explicitly included memory match router at prefix /api/games/memory_match")

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
        
        # 对于API请求，确保我们总是返回JSON而不是HTML
        if url.startswith("/api/") or "json" in request.headers.get("accept", ""):
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error", "error": str(e)}
            )
        # 其他请求返回常规错误响应
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

# Mount static files if directories exist
# Mount meme images directory if it exists
meme_dir = os.path.abspath("backend/datasets/meme")
if os.path.exists(meme_dir):
    app.mount("/memes", StaticFiles(directory=meme_dir), name="memes")

# Simple root endpoint
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Inflowence API</title>
        </head>
        <body>
            <h1>Welcome to the Inflowence API</h1>
            <p>API is up and running!</p>
            <p>Visit <a href="/docs">/docs</a> for the API documentation.</p>
        </body>
    </html>
    """

# Add CORS support for memory match router
@app.options("/api/games/memory_match/{path:path}")
async def memory_match_options(path: str, request: Request):
    logger.info(f"接收到CORS预检请求: {path}")
    return Response(status_code=200)

@app.get("/api/games/memory_match/images/{image_name:path}")
async def proxy_image(image_name: str, request: Request):
    logger.info(f"Memory match image request: {image_name}")
    try:
        # Use the local implementation from memory_match_router
        return await memory_match_router.serve_meme_image(image_filename=image_name)
    except Exception as e:
        logger.error(f"Error serving image: {str(e)}")
        return Response(status_code=500, content=f"Error serving image: {str(e)}")

@app.get("/api/games/memory_match/initialize_game")
async def proxy_initialize_game_get(request: Request):
    logger.info("Memory match game initialization GET request received")
    try:
        # 直接调用独立的GET处理函数
        result = await memory_match_router.initialize_game_data_with_local_urls_get(
            http_request=request
        )
        # 如果返回的是Response对象，直接返回
        if isinstance(result, Response):
            return result
            
        # 否则，确保我们返回一个JSONResponse
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error in memory match initialization GET: {str(e)}")
        # 始终返回JSON格式的错误响应
        return JSONResponse(
            status_code=500,
            content={"detail": f"Error processing game initialization: {str(e)}"}
        )

@app.post("/api/games/memory_match/initialize_game")
async def proxy_initialize_game_post(request: Request):
    logger.info("Memory match game initialization POST request received")
    try:
        # 解析请求体
        body = await request.json()
        
        # 调用专用的POST处理函数
        result = await memory_match_router.initialize_game_data_with_local_urls_post(
            game_request=GameInitRequest(**body),
            http_request=request
        )
        
        # 如果返回的是Response对象，直接返回
        if isinstance(result, Response):
            return result
            
        # 否则，确保我们返回一个JSONResponse
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error in memory match initialization POST: {str(e)}")
        # 始终返回JSON格式的错误响应
        return JSONResponse(
            status_code=500,
            content={"detail": f"Error processing game initialization: {str(e)}"}
        )

# 添加专门的OPTIONS处理器用于initialize_game端点
@app.options("/api/games/memory_match/initialize_game")
async def memory_match_initialize_options():
    logger.info("接收到initialize_game的CORS预检请求")
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Origin, Accept",
            "Access-Control-Max-Age": "3600"
        }
    )

# Add a fallback endpoint for the initialize_game path without /api prefix
@app.post("/games/memory_match/initialize_game")
async def fallback_initialize_game(request: Request):
    logger.info("Fallback initialize_game POST endpoint called - redirecting to /api/games/memory_match/initialize_game")
    try:
        # Get request body
        body = await request.json()
        logger.info(f"Received initialize_game request: {body}")
        
        # 直接调用我们已有的处理程序
        return await proxy_initialize_game_post(request)
    except Exception as e:
        logger.error(f"Error in fallback_initialize_game: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Error processing game initialization: {str(e)}"}
        )

@app.get("/games/memory_match/initialize_game")
async def fallback_initialize_game_get(request: Request):
    logger.info("Fallback initialize_game GET endpoint called - redirecting to /api/games/memory_match/initialize_game")
    try:
        # 直接调用我们的GET处理程序
        return await proxy_initialize_game_get(request)
    except Exception as e:
        logger.error(f"Error in fallback_initialize_game_get: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Error processing game initialization: {str(e)}"}
        )

# Add an OPTIONS handler for the fallback endpoint
@app.options("/games/memory_match/initialize_game")
async def fallback_memory_match_initialize_options():
    logger.info("Received CORS preflight request for fallback initialize_game endpoint")
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Origin, Accept",
            "Access-Control-Max-Age": "3600"
        }
    )

# Add an OPTIONS handler for the fallback path pattern
@app.options("/games/memory_match/{path:path}")
async def fallback_memory_match_options(path: str, request: Request):
    logger.info(f"Received CORS preflight request for fallback path: {path}")
    return Response(status_code=200)

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


