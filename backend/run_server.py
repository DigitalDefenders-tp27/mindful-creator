#!/usr/bin/env python3
"""
Server startup script with environment variable handling
"""
import os
import sys
import uvicorn
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('server')


def main():
    logger.info("=== Starting Mindful Creator Backend Service ===")
logger.info("=== Starting Mindful Creator Backend Service ===")

# Load environment variables from .env file
logger.info("Loading environment variables...")
root_env = os.path.join(os.path.dirname(__file__), os.pardir, ".env")
load_dotenv(root_env)

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql://postgres:DhybdxDhwpiNkqWeySoABQBcMSgbUTJW@maglev.proxy.rlwy.net:17054/railway"
)

# Manually set environment variables if not already set
if not os.environ.get("YOUTUBE_API_KEY"):
    os.environ["YOUTUBE_API_KEY"] = "AIzaSyDU95gTm6jKz85RdDj84QpU1tUETrCCP8M"
    logger.warning("YOUTUBE_API_KEY environment variable not found, using default value")

    
    # Load environment variables
    logger.info("Loading environment variables...")
    load_dotenv()
    
    # Log configuration status
    logger.info("Environment variable configuration status:")
    logger.info(f"- YOUTUBE_API_KEY: {'Set' if os.getenv('YOUTUBE_API_KEY') else 'Not Set'}")
    logger.info(f"- SPACE_API_URL: {'Set' if os.getenv('SPACE_API_URL') else 'Not Set'}")
    logger.info(f"- CORS_ORIGIN: {'Set' if os.getenv('CORS_ORIGIN') else 'Not Set'}")
    
    # Start the FastAPI server
    logger.info("Starting FastAPI server, listening on 0.0.0.0:8002...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8002,
        reload=True
    )

if __name__ == "__main__":
    main() 