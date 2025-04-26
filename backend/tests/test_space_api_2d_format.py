#!/usr/bin/env python3
"""
Test script: Verify Space API comment processing functionality
This script tests:
1. Generate 100 test comments
2. Call Space API to analyze these comments
3. Validate the structure and content of the returned results
"""

import os
import sys
import logging
import time
import random
import asyncio
from typing import List, Dict, Any
from dotenv import load_dotenv

# Ensure project root directory is in Python path
proj_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import Space API analyzer functionality
try:
    from app.api.youtube.analyzer import (
        analyse_comments_with_space_api,
        extract_video_id,
        fetch_youtube_comments
    )
    logger.info("Successfully imported Space API analyzer functionality")
except ImportError as e:
    logger.error(f"Failed to import Space API analyzer functionality: {e}")
    sys.exit(1)

# Load environment variables
load_dotenv(os.path.join(proj_root, '.env'))

# Test comment samples
SAMPLE_COMMENTS = [
    # Positive comments
    "This video was incredibly helpful! Thanks for sharing.",
    "I've been following your channel for a while, and your content keeps getting better!",
    "Very clear explanation, easy to understand.",
    "This is exactly what I needed to hear today. Thank you!",
    "Your videos have been a great help with my studies. Keep it up!",
    "Absolutely loved this content! You've gained a new subscriber.",
    "Best explanation of this topic I've seen anywhere!",
    "You made a complex topic so accessible, thank you!",
    "Your passion for this subject really shines through. Inspiring!",
    "This changed my perspective completely. So grateful!",
    
    # Neutral comments
    "I watched the entire video and learned something new.",
    "Interesting point of view, I hadn't thought about it that way.",
    "Just discovered your channel, will check out more videos.",
    "What camera do you use for filming?",
    "When are you releasing your next video?",
    "I'm curious about your thoughts on the related topic.",
    "Have you considered covering this specific aspect in future videos?",
    "The lighting in this video seems different from your usual setup.",
    "I'm watching this at 1.5x speed to save time.",
    "Found this through the recommendation algorithm.",
    
    # Negative/critical comments
    "This video is way too long for such a simple topic.",
    "You clearly don't know what you're talking about.",
    "I can't believe people actually watch this garbage.",
    "Your voice is so annoying, I couldn't finish the video.",
    "Stop with the clickbait titles, it's really frustrating.",
    "The information in this video is completely wrong. Do your research next time.",
    "This is the worst tutorial I've ever seen. Complete waste of time.",
    "If this is the best you can do, you should quit YouTube.",
    "How do you have so many subscribers with such terrible content?",
    "I hate how fake your enthusiasm is. Just be genuine.",
    "This content is so derivative and adds nothing new to the conversation.",
    "Disappointing quality compared to your earlier videos.",
    "You're just repeating what everyone else says without any original insight.",
    "The audio quality is terrible, I could barely understand you.",
    "You spent more time on sponsors than actual content. Unsubscribed."
]

def generate_test_comments(count: int = 100) -> List[str]:
    """
    Generate a list of test comments by randomly selecting sample comments and adding variations
    
    Parameters:
        count: Number of comments to generate
        
    Returns:
        List of generated comments
    """
    logger.info(f"Generating {count} test comments")
    
    generated_comments = []
    
    # Add some comment variations
    variations = [
        "I agree! {}",
        "{} Thanks for sharing!",
        "Honestly, {}",
        "Wow, {}",
        "I think {} That's my opinion.",
        "{} Keep up the great work!",
        "I'm not sure if I agree. {}",
        "Actually, {}",
        "{} But maybe I'm wrong.",
        "{} I'm sharing this with my friends!",
        "Not to be rude, but {}",
        "As a long-time viewer, {}",
        "First time commenting, but {}",
        "I've watched this twice and {}",
        "From my perspective, {}"
    ]
    
    # Generate random comments
    for _ in range(count):
        base_comment = random.choice(SAMPLE_COMMENTS)
        
        # Randomly decide whether to use a variation or the original comment
        if random.random() < 0.3:  # 30% chance of using a variation
            variation_template = random.choice(variations)
            comment = variation_template.format(base_comment)
        else:
            comment = base_comment
            
        generated_comments.append(comment)
    
    return generated_comments

async def test_space_api():
    """Test Space API comment processing functionality"""
    logger.info("Testing Space API comment processing...")
    
    # Generate 100 test comments
    comments = generate_test_comments(100)
    logger.info(f"Generated {len(comments)} comments")
    
    try:
        # Directly call the imported analysis function
        logger.info("Calling Space API to analyze comments...")
        start_time = time.time()
        
        result = analyse_comments_with_space_api(comments)
            
        duration = time.time() - start_time
        logger.info(f"Space API analysis completed in {duration:.2f} seconds")
        
        # Check results
        if not result or "error" in result:
            error_msg = result.get("error", "Unknown error") if result else "Empty result returned"
            logger.error(f"Space API returned an error: {error_msg}")
            return False
            
        # Validate result structure
        if not result.get("sentiment") or not result.get("toxicity"):
            logger.error(f"Space API returned result with incorrect structure: {result.keys()}")
            return False
            
        # Output analysis result summary
        sentiment = result["sentiment"]
        toxicity = result["toxicity"]
        
        logger.info("=== Sentiment Analysis Results ===")
        logger.info(f"Positive comments: {sentiment.get('positive_count', 0)}")
        logger.info(f"Neutral comments: {sentiment.get('neutral_count', 0)}")
        logger.info(f"Negative comments: {sentiment.get('negative_count', 0)}")
        
        logger.info("=== Toxicity Analysis Results ===")
        logger.info(f"Total toxic comments: {toxicity.get('toxic_count', 0)}")
        logger.info(f"Toxic comments percentage: {toxicity.get('toxic_percentage', 0):.2f}%")
        
        logger.info("=== Toxicity Type Distribution ===")
        toxic_types = toxicity.get("toxic_types", {})
        for t_type, count in toxic_types.items():
            logger.info(f"{t_type}: {count}")
            
        logger.info("✅ Space API test passed")
        return True
            
    except Exception as e:
        logger.error(f"❌ Space API test failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

# Main entry point
if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("Running SPACE API Comment Test")
    logger.info("=" * 50)
    
    # Run async test
    loop = asyncio.get_event_loop()
    success = loop.run_until_complete(test_space_api())
    
    if success:
        logger.info("🎉 Test passed")
        sys.exit(0)
    else:
        logger.error("❌ Test failed")
        sys.exit(1) 