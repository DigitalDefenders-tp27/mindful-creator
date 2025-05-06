#!/usr/bin/env python3
"""
Test script for the new YouTube and OpenRouter client classes.
This script tests the basic functionality of the clients without making actual API calls.
"""

import os
import sys
import time
import logging

# Add the backend directory to the path so we can import the app module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger("test_script")

def main():
    """Main test function to verify client functionality"""
    logger.info("Starting client test")
    
    # Import the clients
    try:
        from app.api.youtube.client import YouTubeClient
        from app.api.openrouter.client import OpenRouterClient
        from app.api.utils.logger import setup_logger
        
        logger.info("Successfully imported client classes")
    except ImportError as e:
        logger.error(f"Failed to import client classes: {e}")
        return
    
    # Test YouTube client
    logger.info("Testing YouTube client")
    yt_client = YouTubeClient()
    
    # Test URL parsing
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://www.youtube.com/embed/dQw4w9WgXcQ"
    ]
    
    for url in test_urls:
        video_id = yt_client.extract_video_id(url)
        logger.info(f"URL: {url} -> Video ID: {video_id}")
    
    # Test OpenRouter client
    logger.info("Testing OpenRouter client")
    or_client = OpenRouterClient()
    
    logger.info(f"API Key configured: {or_client.api_key is not None}")
    logger.info(f"Default model: {or_client.model}")
    
    logger.info("Client test completed")

if __name__ == "__main__":
    main() 