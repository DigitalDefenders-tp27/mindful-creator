#!/usr/bin/env python3
"""
Connectivity and functionality test script for YouTube and Space API.

This script tests:
1. YouTube API connectivity
2. Space API connectivity 
3. Comment analysis functionality with hardcoded comments

Usage:
    python test_connectivity.py
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the backend package to the path
ROOT = Path(__file__).resolve().parents[1] 
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Import the functions from the analyzer module
from app.api.youtube.analyzer import (
    extract_video_id,
    fetch_youtube_comments,
    analyse_comments_with_space_api
)

# Test video URL
TEST_VIDEO_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up

# Hardcoded test comments
TEST_COMMENTS = [
    "This video is amazing! I love the content and production quality.",
    "I don't think this was very good, disappointed with the quality.",
    "Interesting video but nothing special, just average content.",
    "This is absolutely terrible and a waste of time.",
    "What a fantastic video, really enjoyed watching this!",
    "The presenter is so annoying, I couldn't stand listening.",
    "This content promotes harmful stereotypes and should be removed.",
    "I'm going to subscribe because this channel has great content!",
    "Neutral opinion on this one, neither good nor bad.",
    "I hate everything about this video, worst thing I've seen all day."
]

def test_youtube_connectivity() -> bool:
    """
    Test connectivity to YouTube API by fetching video ID and comments.
    
    Returns:
        bool: True if test passes, False otherwise
    """
    logger.info("Testing YouTube API connectivity...")
    
    try:
        # Test video ID extraction
        video_id = extract_video_id(TEST_VIDEO_URL)
        if not video_id:
            logger.error("Failed to extract video ID")
            return False
        
        logger.info(f"Successfully extracted video ID: {video_id}")
        
        # Test comment fetching
        comments = fetch_youtube_comments(TEST_VIDEO_URL, max_comments=5)
        
        if not comments:
            logger.error("Failed to fetch comments")
            return False
        
        logger.info(f"Successfully fetched {len(comments)} comments from YouTube")
        logger.info(f"Sample comment: {comments[0][:100]}...")
        
        return True
        
    except Exception as e:
        logger.error(f"YouTube API test failed: {str(e)}")
        return False

def test_space_connectivity(use_hardcoded: bool = True) -> bool:
    """
    Test connectivity to Space API by analyzing comments.
    
    Args:
        use_hardcoded: Whether to use hardcoded comments or fetch from YouTube
    
    Returns:
        bool: True if test passes, False otherwise
    """
    logger.info("Testing Space API connectivity...")
    
    try:
        # Use either hardcoded comments or fetch from YouTube
        if use_hardcoded:
            comments = TEST_COMMENTS
            logger.info(f"Using {len(comments)} hardcoded test comments")
        else:
            comments = fetch_youtube_comments(TEST_VIDEO_URL, max_comments=10)
            logger.info(f"Fetched {len(comments)} comments from YouTube for testing")
        
        # Test Space API
        start_time = time.time()
        result = analyse_comments_with_space_api(comments)
        elapsed_time = time.time() - start_time
        
        if "error" in result:
            logger.error(f"Space API analysis failed: {result['error']}")
            return False
        
        # Validate result structure
        if not all(key in result for key in ["sentiment", "toxicity"]):
            logger.error(f"Invalid result structure: {result.keys()}")
            return False
        
        logger.info(f"Space API analysis completed in {elapsed_time:.2f} seconds")
        logger.info(f"Sentiment analysis results: {json.dumps(result['sentiment'], indent=2)}")
        logger.info(f"Toxicity analysis results: {json.dumps(result['toxicity'], indent=2)}")
        
        return True
        
    except Exception as e:
        logger.error(f"Space API test failed: {str(e)}")
        return False

def run_all_tests():
    """Run all connectivity and functionality tests."""
    logger.info("Starting connectivity and functionality tests")
    
    # Test YouTube API
    youtube_result = test_youtube_connectivity()
    logger.info(f"YouTube API test {'PASSED' if youtube_result else 'FAILED'}")
    
    # Test Space API with hardcoded comments
    space_result = test_space_connectivity(use_hardcoded=True)
    logger.info(f"Space API test with hardcoded comments {'PASSED' if space_result else 'FAILED'}")
    
    # If all tests pass
    if youtube_result and space_result:
        logger.info("All tests PASSED")
        return True
    else:
        logger.warning("Some tests FAILED")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 