#!/usr/bin/env python3
"""
Test script for the YouTube comment analysis pipeline.
Tests both local NLP model and OpenRouter integration.
"""
import os
import sys
import logging
from typing import List, Dict, Any
import json

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add parent directory to path to allow imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import required modules
from backend.app.api.youtube.analyzer import analyse_comments_with_space_api
from backend.app.api.youtube.llm_handler import analyse_youtube_comments

def test_analysis_pipeline():
    """Test the complete YouTube analysis pipeline."""
    # Sample comments for testing
    test_comments = [
        "This video is absolutely amazing! I've learned so much, thank you!",
        "What a waste of time. This content is terrible and you should be ashamed.",
        "I'm not sure I understand the point you're trying to make here.",
        "You're an idiot if you believe this garbage. Go educate yourself.",
        "The editing is pretty good, but the content could use some improvement.",
    ]
    
    # Step 1: Test local NLP model for sentiment/toxicity analysis
    logger.info("Testing local NLP model...")
    try:
        nlp_result = analyse_comments_with_space_api(test_comments)
        logger.info("Local NLP analysis result:")
        logger.info(f"- Note: {nlp_result.get('note', 'Unknown')}")
        logger.info(f"- Sentiment: {json.dumps(nlp_result.get('sentiment', {}), indent=2)}")
        logger.info(f"- Toxicity: {json.dumps(nlp_result.get('toxicity', {}), indent=2)}")
    except Exception as e:
        logger.error(f"Local NLP analysis failed: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        nlp_result = {"error": str(e)}
    
    # Step 2: Test OpenRouter integration for response strategies
    logger.info("\nTesting OpenRouter integration...")
    try:
        llm_result = analyse_youtube_comments(test_comments)
        logger.info(f"OpenRouter analysis result status: {llm_result.get('status')}")
        
        # Print strategies if available
        strategies = llm_result.get('strategies', '')
        if strategies:
            logger.info("Strategies:")
            for line in strategies.split('\n'):
                if line.strip():
                    logger.info(f"  {line.strip()}")
        else:
            logger.info("No strategies returned")
            
        # Print example responses if available
        example_comments = llm_result.get('example_comments', [])
        if example_comments:
            logger.info(f"Example responses ({len(example_comments)}):")
            for i, item in enumerate(example_comments[:2], 1):  # Show only first 2 for brevity
                logger.info(f"  Example {i}:")
                logger.info(f"    Comment: {item.get('comment', '')[:50]}...")
                logger.info(f"    Response: {item.get('response', '')[:50]}...")
        else:
            logger.info("No example responses returned")
    except Exception as e:
        logger.error(f"OpenRouter analysis failed: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        llm_result = {"error": str(e)}
    
    # Step 3: Combine results (simulation of the API endpoint)
    combined_result = {
        "status": "success" if "error" not in nlp_result and "error" not in llm_result else "partial",
        "total_comments": len(test_comments),
        "analysis": nlp_result,
        "strategies": llm_result.get("strategies", ""),
        "example_comments": llm_result.get("example_comments", []),
        "note": "Test combining local NLP and OpenRouter"
    }
    
    logger.info("\nCombined result structure:")
    for key in combined_result:
        if key not in ["analysis", "strategies", "example_comments"]:
            logger.info(f"- {key}: {combined_result[key]}")
        else:
            logger.info(f"- {key}: [data available]")
    
    return "Test completed"

if __name__ == "__main__":
    print("Starting YouTube analysis pipeline test...\n")
    result = test_analysis_pipeline()
    print(f"\n✅ {result}") 