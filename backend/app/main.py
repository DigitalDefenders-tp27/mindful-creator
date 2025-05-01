import os
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import datetime

from app.api.router import router as api_router
from app.api.relaxation.routes import router as relaxation_router
from app.api.notes.routes import router as notes_router
from app.api.youtube.routes import router as youtube_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("websocket")

# Create FastAPI application
app = FastAPI(
    title="Mindful Creator API",
    description="API for the Mindful Creator application",
    version="0.1.0",
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
    "*"  # Allow all origins as fallback - make sure this is at the end
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://(.*\.)?mindful-creator.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=86400,  # Cache preflight requests for 24 hours
    expose_headers=["Content-Type", "X-API-Version"]
)

# Register routes
app.include_router(data_router, prefix="/api", tags=["data"])
app.include_router(data_router,   prefix="/api/data",    tags=["data"])
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

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint to verify API server is running"""
    return {
        "status": "ok",
        "timestamp": datetime.datetime.now().isoformat(),
        "message": "API server is running"
    }

@app.get("/")
async def root():
    return {"message": "Mindful Creator API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 
