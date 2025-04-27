#!/usr/bin/env python3
"""
Test script: Verify LLM Response Strategies generation

This script tests:
1. LLM connection and functionality for generating response strategies
2. Both strategy generation and example response generation with sample comments
"""

import os
import sys
import logging
import time
from typing import List, Dict, Any
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the backend package to the path
ROOT = Path(__file__).resolve().parents[1] 
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Import the LLM handler directly
try:
    from app.api.youtube.llm_handler import (
        analyse_youtube_comments,
        generate_response_strategies,
        generate_example_responses,
        API_KEY,
        MODEL_NAME
    )
    logger.info("Successfully imported LLM handler functions")
except ImportError as e:
    logger.error(f"Failed to import LLM handler: {e}")
    sys.exit(1)

# Test comments - a mix of different types
TEST_COMMENTS = [
    "This video is absolutely amazing! I learned so much and the production quality is top-notch.",
    "I can't believe how terrible this content is. You clearly don't know what you're talking about.",
    "This explanation was helpful, but I think you missed a few key points worth mentioning.",
    "You're spreading misinformation and should be banned from the platform. This is dangerous content.",
    "I've been following your channel for years and this is by far your best work yet!",
    "Your voice is so annoying, I couldn't make it through the first minute. Learn to speak properly.",
    "Interesting perspective, but I have to respectfully disagree with your main point.",
    "The audio quality in this video is really poor, consider investing in a better microphone.",
    "You've completely changed my mind on this topic. Thank you for the well-researched explanation.",
    "Stop with the clickbait titles! The content doesn't match what you promised in the thumbnail at all."
]

def test_llm_availability():
    """Test if the LLM API credentials are available"""
    if not API_KEY:
        logger.error("API_KEY is not set - please configure OPENROUTER_API_KEY in .env")
        return False
    
    logger.info(f"API_KEY is set, using model: {MODEL_NAME}")
    return True

def test_strategy_generation():
    """Test direct strategy generation function"""
    logger.info("Testing response strategy generation...")
    
    # Take the most critical comments for testing
    critical_comments = TEST_COMMENTS[1:6:2]  # Taking 3 critical comments 
    logger.info(f"Using {len(critical_comments)} critical comments for testing")
    
    start_time = time.time()
    strategy = generate_response_strategies(critical_comments)
    duration = time.time() - start_time
    
    logger.info(f"Strategy generation completed in {duration:.2f} seconds")
    logger.info(f"Generated strategy length: {len(strategy)} characters")
    
    # Check if we got an actual strategy or the error message
    if strategy == "Could not generate specific strategies at this time.":
        logger.error("⚠️ Strategy generation failed with default error message")
        return False
    
    logger.info("Generated strategy preview:")
    logger.info("-" * 50)
    logger.info(strategy[:500] + "..." if len(strategy) > 500 else strategy)
    logger.info("-" * 50)
    
    return True

def test_example_responses():
    """Test example response generation function"""
    logger.info("Testing example response generation...")
    
    # Take a few critical comments
    critical_comments = TEST_COMMENTS[1:4]
    logger.info(f"Using {len(critical_comments)} critical comments for testing")
    
    start_time = time.time()
    examples = generate_example_responses(critical_comments)
    duration = time.time() - start_time
    
    logger.info(f"Example generation completed in {duration:.2f} seconds")
    
    if not examples:
        logger.error("⚠️ Example response generation failed - empty result")
        return False
    
    logger.info(f"Generated {len(examples)} example responses")
    
    # Show the first example
    if examples:
        logger.info("First example response:")
        logger.info("-" * 50)
        logger.info(f"Comment: {examples[0].get('comment', '')}")
        logger.info(f"Response: {examples[0].get('response', '')}")
        logger.info("-" * 50)
    
    return True

def test_full_analysis():
    """Test the full analysis function that combines all steps"""
    logger.info("Testing full comment analysis...")
    
    start_time = time.time()
    result = analyse_youtube_comments(TEST_COMMENTS)
    duration = time.time() - start_time
    
    logger.info(f"Full analysis completed in {duration:.2f} seconds")
    
    if not result or result.get("status") != "success":
        logger.error(f"⚠️ Full analysis failed: {result}")
        return False
    
    # Check if strategies were generated
    strategies = result.get("strategies", "")
    if not strategies or strategies == "Could not generate specific strategies at this time.":
        logger.error("⚠️ Strategies not generated in full analysis")
        return False
    
    # Check if example responses were generated
    examples = result.get("example_comments", [])
    if not examples:
        logger.error("⚠️ Example responses not generated in full analysis")
        return False
    
    logger.info("Full analysis returned both strategies and example responses:")
    logger.info(f"- Strategy length: {len(strategies)} characters")
    logger.info(f"- Example responses: {len(examples)}")
    
    return True

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("TESTING LLM RESPONSE STRATEGY GENERATION")
    logger.info("=" * 60)
    
    # Check if API key is configured
    if not test_llm_availability():
        logger.error("🔑 API key not configured - quitting tests")
        sys.exit(1)
    
    # Run individual function tests
    logger.info("\n1️⃣ Testing direct strategy generation...")
    strategy_success = test_strategy_generation()
    
    logger.info("\n2️⃣ Testing example response generation...")
    examples_success = test_example_responses()
    
    logger.info("\n3️⃣ Testing full analysis function...")
    full_success = test_full_analysis()
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST RESULTS SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Strategy generation: {'✅ PASS' if strategy_success else '❌ FAIL'}")
    logger.info(f"Example responses:   {'✅ PASS' if examples_success else '❌ FAIL'}")
    logger.info(f"Full analysis:       {'✅ PASS' if full_success else '❌ FAIL'}")
    logger.info("=" * 60)
    
    # Exit with appropriate code
    if strategy_success and examples_success and full_success:
        logger.info("🎉 All tests passed successfully!")
        sys.exit(0)
    else:
        logger.error("❌ Some tests failed - check logs for details")
        sys.exit(1) 