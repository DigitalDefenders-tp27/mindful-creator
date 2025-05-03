from fastapi import APIRouter
import time

# Create main API router
router = APIRouter()

@router.get("/")
async def api_root():
    """
    Root endpoint for the API.
    
    Returns:
        dict: A simple message confirming the API is working
    """
    return {
        "status": "ok",
        "message": "Mindful Creator API is available",
        "version": "1.0"
    }

@router.get("/health")
def api_health_check():
    """
    Simple API health check endpoint that always succeeds.
    This endpoint is separate from the main health check and is used by Railway for deployment checks.
    """
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "message": "API is running"
    } 