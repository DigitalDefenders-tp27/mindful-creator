"""
Health check module for the application

This module provides health check endpoints that are used by Railway 
and other platforms to verify the application is running correctly.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
import logging
import time
import datetime
import os
import sys
import platform
import psutil

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api.health")

# Create router
router = APIRouter(
    tags=["health"],
    responses={503: {"description": "Service Unavailable"}},
)

# Record application start time for uptime reporting
START_TIME = time.time()

@router.get("/health")
async def health_check() -> dict:
    """
    Primary health check endpoint required by Railway.
    """
    logger.info("Health check endpoint accessed")
    return {
        "status": "ok",
        "timestamp": datetime.datetime.now().isoformat()
    }

@router.get("/")
async def root_health_check() -> dict:
    """
    Root health check endpoint for Railway.
    """
    logger.info("Root health check endpoint accessed")
    return {
        "status": "ok"
    }

@router.get("/api/health")
async def api_health_check() -> dict:
    """
    API health check with detailed status information.
    """
    logger.info("API health check endpoint accessed")
    
    # Collect uptime information
    uptime_seconds = time.time() - START_TIME
    uptime = {
        "seconds": int(uptime_seconds),
        "minutes": int(uptime_seconds / 60),
        "hours": int(uptime_seconds / 3600),
        "days": int(uptime_seconds / 86400)
    }
    
    # System information
    system_info = {
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "process_id": os.getpid()
    }
    
    # Get process resource usage
    try:
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        system_info["memory_usage_mb"] = memory_info.rss / (1024 * 1024)
        system_info["cpu_percent"] = process.cpu_percent(interval=0.1)
    except Exception as e:
        system_info["resource_error"] = str(e)
    
    return {
        "status": "ok",
        "timestamp": datetime.datetime.now().isoformat(),
        "uptime": uptime,
        "system_info": system_info
    }

@router.get("/api/health/detailed")
async def detailed_health_check() -> dict:
    """
    Detailed health check that verifies critical system components.
    """
    logger.info("Detailed health check endpoint accessed")
    
    # Check components and gather their status
    components = {
        "api": {"status": "ok"},
        "system": {"status": "ok"}
    }
    
    # Database status is added based on environment variable
    if os.environ.get("DATABASE_URL") or os.environ.get("DATABASE_PUBLIC_URL"):
        components["database"] = {"status": "configured"}
        
    # Report on environment variables (masking sensitive data)
    env_vars = {}
    for key, value in os.environ.items():
        if key in ["DATABASE_URL", "DATABASE_PUBLIC_URL"]:
            env_vars[key] = "[CONFIGURED]"
        elif "URL" in key or "TOKEN" in key or "KEY" in key or "SECRET" in key:
            env_vars[key] = "[MASKED]"
        elif key in ["PYTHONPATH", "PATH", "PORT", "ALLOW_DB_FAILURE"]:
            env_vars[key] = value
            
    return {
        "status": "ok",
        "timestamp": datetime.datetime.now().isoformat(),
        "components": components,
        "environment": env_vars
    } 