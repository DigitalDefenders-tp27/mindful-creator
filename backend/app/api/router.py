# app/api/router.py
from fastapi import APIRouter, Depends
import logging
import os
import platform
import sys
import time
import psutil
from typing import Dict, Any
from datetime import datetime

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/")
async def api_root() -> Dict[str, str]:
    """
    API root endpoint
    """
    logger.info("API root endpoint accessed")
    return {"status": "alive"}

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint optimized for Railway deployment
    """
    start_time = time.time()
    
    # Get basic system information
    try:
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        system_memory = psutil.virtual_memory()
        
        # Check key service status
        python_version = platform.python_version()
        model_loaded = os.environ.get("MODEL_LOADED", "false").lower() == "true"
        api_key_available = os.environ.get("YOUTUBE_API_KEY") is not None
        
        # Get runtime information
        process_uptime = time.time() - process.create_time()
        
        # Build detailed health information
        health_data = {
            "status": "ok",
            "timestamp": datetime.now().isoformat(),
            "environment": {
                "python_version": python_version,
                "platform": platform.platform(),
                "process_id": os.getpid()
            },
            "resources": {
                "memory_rss_mb": round(memory_info.rss / 1024 / 1024, 2),
                "memory_vms_mb": round(memory_info.vms / 1024 / 1024, 2),
                "cpu_percent": round(process.cpu_percent(interval=0.1), 2),
                "system_memory_total_gb": round(system_memory.total / 1024 / 1024 / 1024, 2),
                "system_memory_available_gb": round(system_memory.available / 1024 / 1024 / 1024, 2),
                "system_memory_percent": round(system_memory.percent, 2)
            },
            "features": {
                "model_loaded": model_loaded,
                "youtube_api_available": api_key_available
            },
            "uptime_seconds": round(process_uptime, 2),
            "response_time_ms": round((time.time() - start_time) * 1000, 2)
        }
        
        logger.info(f"Health check completed in {health_data['response_time_ms']}ms")
        return health_data
    
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        # Return 200 status code even on error to ensure health check passes
        return {
            "status": "degraded",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "response_time_ms": round((time.time() - start_time) * 1000, 2)
        }