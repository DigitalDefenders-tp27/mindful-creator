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
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("server.log")
    ]
)
logger = logging.getLogger("server")

logger.info("=== Starting Mindful Creator Backend Service ===")

# Load environment variables from .env file
logger.info("Loading environment variables...")
load_dotenv()

# Manually set environment variables if not already set
if not os.environ.get("YOUTUBE_API_KEY"):
    os.environ["YOUTUBE_API_KEY"] = "AIzaSyDU95gTm6jKz85RdDj84QpU1tUETrCCP8M"
    logger.warning("YOUTUBE_API_KEY environment variable not found, using default value")
    
if not os.environ.get("SPACE_API_URL"):
    os.environ["SPACE_API_URL"] = "https://huggingface.co/spaces/your-username/your-space-name/api/predict/"
    logger.warning("SPACE_API_URL environment variable not found, using default value")
    
if not os.environ.get("CORS_ORIGIN"):
    os.environ["CORS_ORIGIN"] = "http://localhost:3000"
    logger.warning("CORS_ORIGIN environment variable not found, using default value")

# Log environment variables for debugging
logger.info(f"Environment variable configuration status:")
logger.info(f"- YOUTUBE_API_KEY: {'Set' if os.environ.get('YOUTUBE_API_KEY') else 'Not set'}")
logger.info(f"- SPACE_API_URL: {'Set' if os.environ.get('SPACE_API_URL') else 'Not set'}")
logger.info(f"- CORS_ORIGIN: {'Set' if os.environ.get('CORS_ORIGIN') else 'Not set'}")

# Start the server
if __name__ == "__main__":
    # Run the FastAPI application with hot reload enabled
    logger.info("Starting FastAPI server, listening on 0.0.0.0:8000...")
    try:
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        logger.exception("Detailed error information:")
        sys.exit(1) 