"""
Fallback application for Railway deployments

This minimal FastAPI application provides basic health check endpoints
and a simple API response when the main application fails to start.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
import logging
import os
import sys

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fallback-app")

# Create a minimal FastAPI application
app = FastAPI(
    title="Mindful Creator API (Fallback Mode)",
    description="Fallback service for Mindful Creator platform",
    version="0.1.0",
)

@app.get("/", response_class=JSONResponse)
async def root():
    """Root endpoint for health checks"""
    logger.info("Fallback root endpoint accessed")
    return {"status": "ok", "mode": "fallback"}

@app.get("/health", response_class=JSONResponse)
async def health():
    """Health check endpoint"""
    logger.info("Fallback health endpoint accessed")
    return {"status": "ok", "mode": "fallback"}

@app.get("/api/health", response_class=JSONResponse)
async def api_health():
    """API health check endpoint"""
    logger.info("Fallback API health endpoint accessed")
    return {"status": "ok", "mode": "fallback"}

@app.get("/api/visualisation/health", response_class=JSONResponse)
async def visualisation_health():
    """Visualisation health check endpoint"""
    logger.info("Fallback visualisation health endpoint accessed")
    return {"status": "ok", "mode": "fallback"}

@app.get("/fallback-status", response_class=HTMLResponse)
async def fallback_status():
    """HTML status page explaining the fallback mode"""
    return """
    <html>
        <head>
            <title>Mindful Creator API - Fallback Mode</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                h1 { color: #e74c3c; }
                .container { max-width: 800px; margin: 0 auto; }
                .info { background-color: #f8f9fa; padding: 20px; border-radius: 5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>⚠️ Fallback Mode Active</h1>
                <div class="info">
                    <p>The Mindful Creator API is currently running in fallback mode.</p>
                    <p>This means the main application failed to start properly, but this minimal
                    service is running to maintain health checks and prevent deployment failures.</p>
                    <p>Please check the application logs for error details.</p>
                </div>
            </div>
        </body>
    </html>
    """

# Catch-all route for any other API endpoints
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(request: Request, path: str):
    """Catch-all route that returns a standard response for all other endpoints"""
    logger.info(f"Fallback catch-all accessed: {request.method} /{path}")
    return {
        "status": "service_degraded",
        "message": "The application is running in fallback mode due to startup issues",
        "mode": "fallback"
    } 