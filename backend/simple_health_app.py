#!/usr/bin/env python3
"""
Simple FastAPI application to test health check endpoints

Run this with: python3 -m uvicorn simple_health_app:app --port 8000
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import os

app = FastAPI()

@app.get("/")
async def root():
    """Root endpoint for health checks"""
    return {"status": "ok"}

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}

@app.get("/api/health")
async def api_health():
    """API health check endpoint"""
    return {"status": "ok"}

@app.get("/api/visualisation/health")
async def visualisation_health():
    """Visualisation health check endpoint"""
    return {"status": "ok"}

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting simple health app on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port) 