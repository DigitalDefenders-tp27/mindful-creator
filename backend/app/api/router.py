# app/api/router.py
from fastapi import APIRouter
import time

router = APIRouter()

@router.get("/", include_in_schema=False)
async def api_root():
    """Simple “alive” message at /api/"""
    return {
        "status": "ok",
        "message": "Mindful Creator API is available",
        "version": "1.0"
    }

@router.get("/health", include_in_schema=False)
async def api_health_check():
    """Railway health-check endpoint → /api/health"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "message": "API is running"
    }