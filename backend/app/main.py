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
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.routing import APIRouter
import datetime
import uvicorn
import platform
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import affirmations, breaths, journals, memes, ratings
from app.routes import data_fetch_orm
from starlette.middleware.base import BaseHTTPMiddleware

# Configure logging VERY EARLY, before other imports if possible
# This ensures all startup messages are captured
logging.basicConfig(
    level=logging.DEBUG,  # Use DEBUG for more verbose output during startup
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout) # Ensure logs go to stdout
    ]
)
logger = logging.getLogger("mindful-creator.startup")
logger.info("Logger configured at DEBUG level for startup.")

logger.info("Starting imports for FastAPI and related modules...")
try:
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Request, Response
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse, HTMLResponse
    from fastapi.routing import APIRouter
    import datetime
    import uvicorn
    import platform
    from dotenv import load_dotenv
    from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates
    logger.info("FastAPI core imports successful.")
except Exception as e:
    logger.critical(f"Failed to import FastAPI core components: {e}", exc_info=True)
    raise

logger.info("Importing application routers...")
try:
    from app.routers import affirmations, breaths, journals, memes, ratings
    from app.routes import data_fetch_orm
    logger.info("Application-specific routers (affirmations, etc.) imported.")
except Exception as e:
    logger.critical(f"Failed to import application-specific routers: {e}", exc_info=True)
    raise

logger.info("Importing Starlette middleware...")
try:
    from starlette.middleware.base import BaseHTTPMiddleware
    logger.info("Starlette middleware imported.")
except Exception as e:
    logger.critical(f"Failed to import Starlette middleware: {e}", exc_info=True)
    raise

logger.info("Initializing FastAPI app object...")
app = FastAPI(
    title="Mindful Creator API",
    description="API for Mindful Creator platform",
    version="0.1.0",
)
logger.info("FastAPI app object initialized.")

logger.info("Including data_fetch_orm router...")
try:
    app.include_router(data_fetch_orm.router, prefix="/api")
    logger.info("data_fetch_orm router included.")
except Exception as e:
    logger.critical(f"Failed to include data_fetch_orm router: {e}", exc_info=True)
    raise


# Optional: CORS middleware
logger.info("Adding CORS middleware...")
try:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # You can restrict this to your frontend origin
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info("CORS middleware added.")
except Exception as e:
    logger.critical(f"Failed to add CORS middleware: {e}", exc_info=True)
    raise

logger.info("Importing API routers (games, health, api, youtube, visualisation)...")
try:
    # Explicitly import the games router
    from app.api.games import router as games_api_router 
    logger.info("Games API router imported.")
    # Import routers, with health check router first to ensure it's available early
    from app.api.health import router as health_router  # Import health check router first
    logger.info("Health API router imported.")
    from app.api.router import router as api_router
    logger.info("Base API router imported.")
    from app.api.youtube.routes import router as youtube_router
    logger.info("YouTube API router imported.")
    from app.api.visualisation.routes import router as visualisation_router
    logger.info("Visualisation API router imported.")
    sys.stdout.flush() # Ensure previous log is flushed
    print("[DEBUG PRINT IN MAIN.PY] Reached point immediately after Visualisation API router import.", file=sys.stderr, flush=True)
except Exception as e:
    logger.critical(f"Failed to import one or more API routers: {e}", exc_info=True)
    raise

logger.info("Loading .env variables...")
try:
    load_dotenv()
    logger.info(".env variables loaded.")
except Exception as e:
    logger.warning(f"Failed to load .env file (this might be normal in production): {e}")


# Reconfigure logger for the main application if needed, or use the startup logger
# For consistency, let's ensure the mindful-creator logger also logs to stdout
app_logger = logging.getLogger("mindful-creator")
app_logger.setLevel(logging.DEBUG) # Or logging.INFO for less verbosity
if not any(isinstance(h, logging.StreamHandler) for h in app_logger.handlers):
    app_logger.addHandler(logging.StreamHandler(sys.stdout))


logger.info("Checking environment variables...")
# Check environment variables
ALLOW_DB_FAILURE = os.getenv("ALLOW_DB_FAILURE", "false").lower() == "true"
DATABASE_CONNECT_TIMEOUT = int(os.getenv("DATABASE_CONNECT_TIMEOUT", "30"))
APP_STARTUP_TIMEOUT = int(os.getenv("APP_STARTUP_TIMEOUT", "20")) # This was 20 in user log

# Get and log database URLs
DATABASE_PUBLIC_URL = os.getenv("DATABASE_PUBLIC_URL")
DATABASE_URL = os.getenv("DATABASE_URL")

logger.info(f"DATABASE_PUBLIC_URL: {'[SET]' if DATABASE_PUBLIC_URL else '[NOT SET]'}")
logger.info(f"DATABASE_URL: {'[SET]' if DATABASE_URL else '[NOT SET]'}")
logger.info(f"ALLOW_DB_FAILURE: {ALLOW_DB_FAILURE}")
logger.info(f"DATABASE_CONNECT_TIMEOUT: {DATABASE_CONNECT_TIMEOUT}")
logger.info(f"APP_STARTUP_TIMEOUT: {APP_STARTUP_TIMEOUT}") # Log the actual value being used

# Record startup time
start_time = time.time()
logger.info(f"====== MINDFUL CREATOR BACKEND STARTING (detailed log) ======")
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

logger.info("Logging initial system resources...")
log_system_resources()


# Configure CORS middleware (already added, this is a note)
logger.info("Setting up allowed origins for CORS...")
allowed_origins = [
    "http://localhost:3000",  # Local development (frontend)
    "http://localhost:5173",  # Vite dev server (frontend)
    "https://mindful-creator.vercel.app",  # Main Vercel production domain
    "https://tiezhu.org", # Custom domain
    "https://www.tiezhu.org" # Custom domain with www
    # Add any other specific production/staging domains here
]
vercel_preview_regex = r"^https://mindful-creator-[a-zA-Z0-9\\-]+-tp27\\.vercel\\.app$"
# Middleware already added, this logging confirms the values used.
logger.info(f"CORS Allowed Origins: {allowed_origins}")
logger.info(f"CORS Vercel Preview Regex: {vercel_preview_regex}")


logger.info("Importing HuggingFace Transformers and PyTorch...")
try:
    from transformers import AutoTokenizer
    import torch # Keep this import with transformers
    logger.info("HuggingFace Transformers and PyTorch imported.")
except Exception as e:
    logger.critical(f"Failed to import Transformers or PyTorch: {e}", exc_info=True)
    raise


# === Model / tokenizer paths ===================================================
TOKENIZER_DIR = "/app/bert-base-uncased"   # Base BERT already downloaded in Dockerfile
MODEL_DIR     = "/app/nlp"                 # Cloned CommentResponse space
WEIGHTS_FILE  = os.path.join(MODEL_DIR, "pytorch_model.bin")
CFG_FILE      = os.path.join(MODEL_DIR, "config.json")
logger.info(f"NLP Model Paths: TOKENIZER_DIR={TOKENIZER_DIR}, MODEL_DIR={MODEL_DIR}")

@app.on_event("startup")
async def load_nlp_model():
    logger.info("Executing NLP model startup event...")
    t0 = time.time()
    try:
        logger.info("Verifying NLP model key paths...")
        for p in (TOKENIZER_DIR, MODEL_DIR, WEIGHTS_FILE, CFG_FILE):
            if not os.path.exists(p):
                logger.error(f"NLP Startup: Missing file/dir: {p}")
                raise FileNotFoundError(f"Missing file/dir: {p}")
        logger.info("NLP model key paths verified.")

        logger.info(f"NLP Startup: Loading tokenizer from {TOKENIZER_DIR}")
        tokenizer = AutoTokenizer.from_pretrained(
            TOKENIZER_DIR,
            local_files_only=True
        )
        logger.info("NLP Startup: Tokenizer loaded.")

        logger.info("NLP Startup: Dynamically importing CommentMTLModel...")
        if MODEL_DIR not in sys.path:
            sys.path.insert(0, MODEL_DIR)
        from model import CommentMTLModel  # noqa: E402
        logger.info("NLP Startup: CommentMTLModel imported.")

        logger.info(f"NLP Startup: Reading config from {CFG_FILE}")
        with open(CFG_FILE, "r") as f:
            cfg = json.load(f)
        logger.info("NLP Startup: Config loaded.")

        model = CommentMTLModel(
            model_name=TOKENIZER_DIR,
            num_sentiment_labels=cfg["num_sentiment_labels"],
            num_toxicity_labels=cfg["num_toxicity_labels"],
            dropout_prob=cfg.get("dropout_prob", 0.1)
        )
        logger.info("NLP Startup: CommentMTLModel initialized.")

        logger.info(f"NLP Startup: Loading model weights from {WEIGHTS_FILE}")
        state_dict = torch.load(WEIGHTS_FILE, map_location="cpu")
        model.load_state_dict(state_dict, strict=False)
        model.eval()
        logger.info("NLP Startup: Model weights loaded and model set to eval mode.")

        app.state.tokenizer    = tokenizer
        app.state.model        = model
        app.state.model_loaded = True
        logger.info(f"✅ NLP model ready ({time.time()-t0:.2f}s)")

    except Exception as exc:
        app.state.model_loaded     = False
        app.state.model_load_error = str(exc)
        logger.critical(f"❌ Failed to load NLP model: {exc}", exc_info=True)
        # Depending on ALLOW_DB_FAILURE or a new specific flag, you might raise here or allow continuation

logger.info("Including health_router...")
try:
    app.include_router(health_router)  # No prefix, to allow root-level health checks
    logger.info("health_router included.")
except Exception as e:
    logger.critical(f"Failed to include health_router: {e}", exc_info=True)
    raise

logger.info("Including youtube_router...")
try:
    app.include_router(youtube_router, prefix="/api")
    logger.info("youtube_router included.")
except Exception as e:
    logger.critical(f"Failed to include youtube_router: {e}", exc_info=True)
    raise

logger.info("Including visualisation_router...")
try:
    app.include_router(visualisation_router, prefix="") # Ensure this prefix is intended
    logger.info("visualisation_router included.")
except Exception as e:
    logger.critical(f"Failed to include visualisation_router: {e}", exc_info=True)
    raise

logger.info("All core routers (health, youtube, visualisation) registered.")

# Health check endpoints have been moved to app/api/health.py
# No additional health check endpoints needed here since we include the health_router
logger.info("Health check endpoints are now managed by health_router.")


logger.info("Defining NLP diagnostics endpoint...")
@app.get("/api/diagnostics/nlp")
async def nlp_diagnostics() -> Dict[str, Any]:
    logger.info("NLP DIAGNOSTICS ENDPOINT ACCESSED")
    # ... (rest of the function remains the same)
# ... (rest of main.py remains the same, ensure logging is consistent)

    # Check model path
    model_path_exists = os.path.exists(MODEL_DIR) # Corrected from MODEL_PATH
    
    # List directory contents
    app_contents = []
    nlp_contents = []
    try:
        app_contents = os.listdir("/app")
        if model_path_exists:
            nlp_contents = os.listdir(MODEL_DIR)
    except Exception as e:
        logger.error(f"Failed to list directories: {e}")
    
    # Collect diagnostic information
    diagnostics = {
        "timestamp": datetime.datetime.now().isoformat(),
        "model_path_tokenizer": TOKENIZER_DIR, # More specific
        "model_path_custom_model": MODEL_DIR,    # More specific
        "model_path_exists": model_path_exists, # This refers to MODEL_DIR
        "tokenizer_dir_exists": os.path.exists(TOKENIZER_DIR),
        "weights_file_exists": os.path.exists(WEIGHTS_FILE),
        "cfg_file_exists": os.path.exists(CFG_FILE),
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
logger.info("NLP diagnostics endpoint defined.")

logger.info("Checking MODEL_LOADED environment variable...")
model_loaded_env = os.environ.get("MODEL_LOADED", "false").lower() == "true" # Renamed to avoid conflict
logger.info(f"MODEL_LOADED environment variable: {os.environ.get('MODEL_LOADED', 'not set')}")
logger.info(f"Model loaded status from env var: {model_loaded_env}")


logger.info("Defining ADDITIONAL_ROUTES list...")
ADDITIONAL_ROUTES = [
    ("app.api.relaxation.routes", "/api/relaxation"),
    ("app.api.notes.routes", "/api/notes"),
    # ("app.api.youtube.routes", "/api/youtube"), # Already included
    ("app.api.copyright.routes", "/api/copyright"),
    ("app.routers.affirmations", "/api/affirmations"),
    ("app.routers.breaths", "/api/breaths"),
    ("app.routers.journals", "/api/journals"),
    ("app.routers.memes", "/api/memes"),
    # ("app.routers.ratings", "/api/ratings") # Already included below
]
logger.info("ADDITIONAL_ROUTES list defined.")

logger.info("Including games_api_router...")
try:
    app.include_router(games_api_router, prefix="/api/games")
    logger.info("games_api_router included.")
except Exception as e:
    logger.critical(f"Failed to include games_api_router: {e}", exc_info=True)
    # Decide if this is critical enough to raise

logger.info("Including ratings.router...")
try:
    app.include_router(ratings.router, prefix="/api/ratings")
    logger.info("ratings.router included.")
except Exception as e:
    logger.critical(f"Failed to include ratings.router: {e}", exc_info=True)
    # Decide if this is critical enough to raise


logger.info("Loading additional routes from ADDITIONAL_ROUTES list...")
for route_module, prefix in ADDITIONAL_ROUTES:
    try:
        module_start_time = time.time()
        logger.info(f"Attempting to load route module: {route_module} with prefix {prefix}")
        module = importlib.import_module(route_module)
        
        if hasattr(module, "router"):
            logger.info(f"Including router from {route_module} at prefix {prefix}")
            app.include_router(module.router, prefix=prefix)
            logger.info(f"Successfully loaded and included router from {route_module} in {time.time() - module_start_time:.2f} seconds")
        else:
            logger.warning(f"Module {route_module} does not have a 'router' attribute.")
    except ImportError as ie:
        logger.error(f"ImportError for {route_module}: {str(ie)}", exc_info=True)
        # Potentially raise or handle if ALLOW_DB_FAILURE is false and module is critical
    except Exception as e:
        logger.error(f"Failed to load {route_module}: {str(e)}", exc_info=True)
        # Potentially raise or handle
logger.info("Finished loading additional routes.")

logger.info("Adding HTTP middleware for process time header...")
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
# ... (rest of middleware)
    _start_time = time.time() # Use a different variable name
    method = request.method
    url = request.url.path
    
    logger.debug(f"Request started: {method} {url}") # Changed to debug
    
    try:
        response = await call_next(request)
        process_time = time.time() - _start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        status_code = response.status_code
        logger.info(f"Request completed: {method} {url} - Status: {status_code} - Time: {process_time:.4f}s")
        return response
    except Exception as e:
        process_time = time.time() - _start_time
        logger.error(f"Request failed: {method} {url} - Error: {str(e)} - Time: {process_time:.4f}s", exc_info=True)
        # Return a generic error response but ensure it's valid JSONResponse
        return JSONResponse(
            status_code=500, # Or appropriate error code
            content={"detail": "Internal Server Error processing request", "error_context": str(e)}
        )
logger.info("HTTP middleware for process time header added.")


# Record application startup completion
startup_duration = time.time() - start_time # Renamed from startup_time
logger.info(f"====== MINDFUL CREATOR BACKEND STARTED in {startup_duration:.2f} seconds ======")
port = int(os.environ.get("PORT", 8000)) # Define port here before it's used in if __name__
logger.info(f"API available at http://0.0.0.0:{port}")
logger.info("Logging system resources after startup...")
log_system_resources()

logger.info("Mounting static files for memes...")
meme_dir = os.path.abspath("backend/datasets/meme") # This path might be an issue in Docker
# Correct path within Docker should be relative to /app
docker_meme_dir = "/app/datasets/meme" 
if os.path.exists(docker_meme_dir): # Check corrected path
    app.mount("/memes", StaticFiles(directory=docker_meme_dir), name="memes")
    logger.info(f"Mounted static files for memes from {docker_meme_dir}")
else:
    logger.warning(f"Meme directory {docker_meme_dir} not found. Memes will not be served.")


logger.info("Defining /welcome HTML endpoint...")
@app.get("/welcome", response_class=HTMLResponse)
async def welcome_page():
# ... (rest of welcome_page)
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
logger.info("/welcome HTML endpoint defined.")

logger.info("Adding LoggingMiddleware...")
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
# ... (rest of LoggingMiddleware)
        __start_time = time.time() # Different var name
        response = await call_next(request)
        process_time = time.time() - __start_time
        logger.info(f"Request (via LoggingMiddleware): {request.method} {request.url.path} - Completed in {process_time:.4f}s")
        return response

app.add_middleware(LoggingMiddleware)
logger.info("LoggingMiddleware added.")

logger.info("Defining global exception handler...")
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
# ... (rest of global_exception_handler)
    logger.critical(f"Global unhandled exception: {exc}", exc_info=True) # Changed to critical
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error - Unhandled", "detail": str(exc)},
    )
logger.info("Global exception handler defined.")

logger.info("Checking if script is run as main...")
if __name__ == "__main__":
    logger.info(f"Starting Uvicorn server directly (main.py is __main__) on port {port}")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        log_level="debug", # Use debug for more Uvicorn output
        workers=1, # Keep workers to 1 for easier debugging of startup
        timeout_keep_alive=65
    )
else:
    logger.info("main.py is imported, not run as main. Uvicorn will be started by railway_startup.sh or similar.")

logger.info("End of main.py reached.")


