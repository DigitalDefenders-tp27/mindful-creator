import os
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.api.youtube.routes import router as youtube_router
from app.api.data.routes import router as data_router
from .routes import relaxation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("websocket")

# Create FastAPI application
app = FastAPI(
    title="Mindful Creator API",
    description="YouTube Comment Analysis API",
    version="1.0.0"
)

# Configure CORS
origins = [
    os.getenv("CORS_ORIGIN", "http://localhost:3000"),
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "https://mindful-creator-awoc.vercel.app",
    "https://mindful-creator-mymc.vercel.app",
    "https://mindful-creator-99fvqeosu-tp27.vercel.app",
    "https://mindful-creator.vercel.app",
    "https://mindful-creator-gwnq.vercel.app",
    "https://mindful-creator-murex.vercel.app",
    "https://mindful-creator-tp27.vercel.app",
    # Allow all origins as fallback
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(youtube_router, prefix="/api/youtube", tags=["youtube"])
app.include_router(data_router, prefix="/api", tags=["data"])
app.include_router(relaxation.router, prefix="/api", tags=["relaxation"])

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

# Add a test endpoint to check WebSocket availability
@app.get("/ws-test")
async def websocket_test():
    return {"status": "WebSocket endpoint is available"}

@app.get("/")
async def root():
    return {"message": "Mindful Creator API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 
