from fastapi import APIRouter

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