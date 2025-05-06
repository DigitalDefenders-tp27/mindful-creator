#!/usr/bin/env python3
"""
OpenRouter API Test Script
This script tests connectivity and functionality of the OpenRouter API by sending
10 diverse test comments and checking the response.
"""

import os
import sys
import json
import logging
import requests
import time
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = os.getenv('OPENROUTER_MODEL', 'deepseek/deepseek-prover-v2:free')

def test_openrouter_connection():
    """Test if we can connect to the OpenRouter API."""
    if not OPENROUTER_API_KEY:
        logger.error("OPENROUTER_API_KEY not found in environment variables")
        return False
    
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello world!"}
            ],
            "max_tokens": 50  # 设置较小的token限制以减少API调用成本
        }
        
        logger.info(f"Testing connection to OpenRouter API with model {MODEL_NAME}...")
        logger.info(f"API key configured: {bool(OPENROUTER_API_KEY)}")
        logger.info(f"API key first 8 chars: {OPENROUTER_API_KEY[:8]}...")
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            message = data.get('choices', [{}])[0].get('message', {}).get('content', '')
            logger.info(f"OpenRouter API response: {message}")
            return True
        else:
            logger.error(f"API request failed with status code {response.status_code}: {response.text}")
            return False
    
    except Exception as e:
        logger.error(f"Error testing OpenRouter connection: {e}")
        return False

def generate_example_response(comment):
    """Test generating an example response for a comment."""
    if not OPENROUTER_API_KEY:
        logger.error("OPENROUTER_API_KEY not found in environment variables")
        return None
    
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""This is a critical comment on my YouTube video:

"{comment}"

Write a thoughtful, professional response that:
1. Acknowledges the comment without being defensive
2. Maintains a positive tone
3. Provides minimal clarification if needed
4. Ends with a forward-looking statement

KEEP IT EXTREMELY BRIEF. Maximum 50 words total. Be direct and to the point.
Use Australian English phrasing where appropriate.
"""
        
        system_message = """You are a professional community manager who specialises in crafting 
extremely concise responses to difficult social media comments. Your responses are authentic and clear,
but prioritize brevity above all else. Keep responses under 50 words. Use Australian English phrasing 
where appropriate."""
        
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 100,  # 减少token数以减少API调用成本
            "temperature": 0.4
        }
        
        logger.info(f"Generating response for comment: {comment[:50]}...")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        
        if response.status_code == 200:
            data = response.json()
            content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
            logger.info(f"Raw content: {content[:100]}...")
            
            # Just return the raw content as the response
            if content and len(content.strip()) > 0:
                return content.strip()
            else:
                logger.warning("Empty content returned")
                return None
        else:
            logger.error(f"API request failed with status code {response.status_code}: {response.text}")
            return None
    
    except Exception as e:
        logger.error(f"Error generating example response: {e}")
        return None

def main():
    """Main function to test OpenRouter API."""
    logger.info("Starting OpenRouter API test...")
    
    # Test connection
    if not test_openrouter_connection():
        logger.error("Failed to connect to OpenRouter API")
        sys.exit(1)
    
    # Test generating example responses for multiple comments
    test_comments = [
        "This video is terrible, you clearly don't know what you're talking about!",
        "I disagree with several points in this video. Your research seems sloppy.",
        "I've been following you for years, but the quality has really gone downhill.",
        "Why do you keep making videos on topics you know nothing about?",
        "Your voice is so annoying, I couldn't even finish watching.",
        "Great content as always, but I noticed a few factual errors you might want to fix.",
        "I don't understand why people watch your videos, they're so boring.",
        "You promised to cover this topic in detail but barely scratched the surface.",
        "Stop clickbaiting with your thumbnails and titles!",
        "Your editing is getting worse with each video. Maybe hire a professional?"
    ]
    
    success_count = 0
    for i, comment in enumerate(test_comments):
        logger.info(f"Testing comment {i+1}/{len(test_comments)}")
        
        response = generate_example_response(comment)
        if response:
            logger.info(f"Generated response: {response}")
            success_count += 1
        else:
            logger.error(f"Failed to generate response for comment: {comment[:50]}...")
        
        # Add a small delay between requests
        if i < len(test_comments) - 1:
            time.sleep(2)
    
    logger.info(f"Successfully generated {success_count}/{len(test_comments)} responses")
    
    if success_count >= 3:  # Consider it a success if we generate at least 3 responses
        logger.info(f"Test passed with {success_count}/{len(test_comments)} successful responses!")
        return 0
    else:
        logger.warning(f"Test failed with only {success_count}/{len(test_comments)} successful responses")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 