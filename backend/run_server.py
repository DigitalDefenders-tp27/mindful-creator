#!/usr/bin/env python3
"""
Server startup script with environment variable handling
"""
import os
import sys
import uvicorn
import logging
import argparse
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('server')


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Start the Mindful Creator backend server")
    parser.add_argument("--port", type=int, default=8080, help="Port to run the server on (default: 8080)")
    args = parser.parse_args()
    
    logger.info("=== Starting Mindful Creator Backend Service ===")
    
    # Load environment variables
    logger.info("Loading environment variables...")
    load_dotenv()
    
    # Log configuration status
    logger.info("Environment variable configuration status:")
    logger.info(f"- YOUTUBE_API_KEY: {'Set' if os.getenv('YOUTUBE_API_KEY') else 'Not Set'}")
    logger.info(f"- SPACE_API_URL: {'Set' if os.getenv('SPACE_API_URL') else 'Not Set'}")
    logger.info(f"- CORS_ORIGIN: {'Set' if os.getenv('CORS_ORIGIN') else 'Not Set'}")
    
    # Start the FastAPI server
    logger.info(f"Starting FastAPI server, listening on 0.0.0.0:{args.port}...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=args.port,
        reload=True
    )

if __name__ == "__main__":
    main() 