#!/usr/bin/env python3
"""
OpenRouter API Test Script
This script tests connectivity and functionality of the OpenRouter API by sending
10 diverse test comments and checking the response.
"""

import os
import sys
import json
import requests
import time
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# OpenRouter API settings
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Test comments with various sentiments and content
TEST_COMMENTS = [
    # Positive comments
    "This video was absolutely brilliant! I learned so much and the production quality was top-notch.",
    "Love your content, mate! Been following for years and you just keep getting better.",
    
    # Neutral comments
    "I'm wondering if you could do a follow-up video on this topic? There's a lot more to explore.",
    "What camera setup do you use for these videos? The quality seems really good.",
    
    # Negative comments
    "Sorry, but this wasn't your best work. The sound quality was poor and the content felt rushed.",
    "Disappointed with this video. You usually provide more in-depth information.",
    
    # Toxic/problematic comments
    "This is absolute garbage! You clearly have no idea what you're talking about.",
    "You should just quit making videos. Nobody cares about your stupid opinions.",
    
    # Mixed sentiment
    "Good points about the topic, but your presentation style is really annoying.",
    "The content is great as usual, but please fix the audio issues in your videos."
]

def test_openrouter_connection():
    """Test basic connectivity to OpenRouter API"""
    if not OPENROUTER_API_KEY:
        logger.error("OPENROUTER_API_KEY not found in environment variables")
        return False
    
    try:
        # Simple test request
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://mindful-creator.vercel.app",
            "X-Title": "Mindful Creator API Test"
        }
        
        test_payload = {
            "model": "deepseek/deepseek-prover-v2:free",  # Using deepseek model for the test
            "messages": [
                {"role": "user", "content": "Hello, is this connection working?"}
            ]
        }
        
        logger.info("Testing basic OpenRouter connectivity...")
        response = requests.post(
            url=OPENROUTER_URL,
            headers=headers,
            data=json.dumps(test_payload)
        )
        
        if response.status_code == 200:
            logger.info("✅ OpenRouter API connection successful!")
            return True
        else:
            logger.error(f"❌ OpenRouter API connection failed. Status code: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ OpenRouter API connection test failed with error: {str(e)}")
        return False

def test_with_comments():
    """Send test comments to OpenRouter API and analyze responses"""
    if not OPENROUTER_API_KEY:
        logger.error("OPENROUTER_API_KEY not found in environment variables")
        return
    
    # First check connection
    if not test_openrouter_connection():
        logger.error("Skipping comment tests due to connection failure")
        return
    
    # Headers for API requests
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://mindful-creator.vercel.app",
        "X-Title": "Mindful Creator API Test"
    }
    
    # Test prompt for analyzing comments
    system_prompt = """
    You are an AI assistant specialized in analyzing YouTube comments.
    For each comment, provide:
    1. A sentiment classification (Positive, Negative, Neutral)
    2. Toxicity assessment (Non-toxic, Mildly toxic, Very toxic)
    3. A brief suggestion on how a content creator should respond
    Format your response as JSON with these fields.
    """
    
    # Process each test comment
    results = []
    
    for i, comment in enumerate(TEST_COMMENTS):
        logger.info(f"Testing comment {i+1}/{len(TEST_COMMENTS)}")
        
        try:
            payload = {
                "model": "deepseek/deepseek-prover-v2:free",  # Using deepseek model
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Please analyze this YouTube comment: \"{comment}\""}
                ]
            }
            
            logger.info(f"Sending request to OpenRouter API...")
            start_time = time.time()
            
            response = requests.post(
                url=OPENROUTER_URL,
                headers=headers,
                data=json.dumps(payload)
            )
            
            elapsed_time = time.time() - start_time
            
            if response.status_code == 200:
                response_data = response.json()
                
                # Extract the assistant's response
                assistant_response = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                try:
                    # Try to parse JSON response if possible
                    try:
                        analysis = json.loads(assistant_response)
                    except json.JSONDecodeError:
                        # If not JSON, use the raw response
                        analysis = {"raw_analysis": assistant_response}
                    
                    result = {
                        "comment": comment,
                        "analysis": analysis,
                        "api_response_time": f"{elapsed_time:.2f}s",
                        "model": response_data.get("model", "unknown")
                    }
                    
                    results.append(result)
                    logger.info(f"✅ Analysis received in {elapsed_time:.2f}s")
                except Exception as e:
                    logger.error(f"❌ Failed to process response: {str(e)}")
                    results.append({
                        "comment": comment,
                        "error": "Processing error",
                        "raw_response": assistant_response
                    })
            else:
                logger.error(f"❌ Request failed with status code {response.status_code}")
                logger.error(f"Response: {response.text}")
                results.append({
                    "comment": comment,
                    "error": f"API Error: {response.status_code}",
                    "response": response.text
                })
            
            # Slight delay to avoid rate limits
            time.sleep(1)
                
        except Exception as e:
            logger.error(f"❌ Error processing comment: {str(e)}")
            results.append({
                "comment": comment,
                "error": str(e)
            })
    
    # Save results to file
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_file = f"openrouter_test_results_{timestamp}.json"
    
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"Test results saved to {output_file}")
    
    # Print summary
    success_count = len([r for r in results if "error" not in r])
    logger.info(f"Summary: {success_count}/{len(TEST_COMMENTS)} comments processed successfully")
    
    return results

if __name__ == "__main__":
    logger.info("Starting OpenRouter API tests...")
    test_results = test_with_comments()
    logger.info("Tests completed!") 