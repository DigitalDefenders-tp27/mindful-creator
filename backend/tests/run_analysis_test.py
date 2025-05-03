import os
import sys
import logging
import requests
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ensure the parent directory is in the Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from app.api.youtube.analyzer import fetch_youtube_comments, analyse_comments_with_local_model
from app.api.youtube.llm_handler import analyse_youtube_comments


def run_test():
    """Run a test of the YouTube comment analysis pipeline"""
    logger.info("=== Starting YouTube analysis test ===")
    
    # Test parameters
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up
    max_comments = 10  # Keep small for testing
    
    # Step 1: Test fetching YouTube comments
    logger.info("\n=== Step 1: Fetching YouTube comments ===")
    try:
        comments = fetch_youtube_comments(video_url, max_comments)
        logger.info(f"Successfully fetched {len(comments)} comments")
        
        # Print a sample of the comments
        for i, comment in enumerate(comments[:3]):
            preview = comment[:100] + "..." if len(comment) > 100 else comment
            logger.info(f"Comment {i+1}: {preview}")
    except Exception as e:
        logger.error(f"Failed to fetch YouTube comments: {e}")
        return
    
    # Step 2: Test local NLP model
    logger.info("\n=== Step 2: Testing local NLP model ===")
    try:
        local_result = analyse_comments_with_local_model(comments)
        logger.info("Local NLP model analysis response:")
        logger.info(json.dumps(local_result, indent=2))
    except Exception as e:
        logger.error(f"Failed to analyze comments with local NLP model: {e}")
    
    # Step 3: Test OpenRouter analysis
    logger.info("\n=== Step 3: Testing OpenRouter analysis ===")
    try:
        router_result = analyse_youtube_comments(comments)
        logger.info("OpenRouter analysis response:")
        
        # Print status and strategies (truncated for readability)
        logger.info(f"Status: {router_result.get('status')}")
        if 'strategies' in router_result:
            strategies = router_result['strategies']
            logger.info(f"Strategies: {strategies[:200]}..." if len(strategies) > 200 else strategies)
        
        # Print example comments if available
        if 'example_comments' in router_result and router_result['example_comments']:
            logger.info(f"Example comments: {len(router_result['example_comments'])} provided")
            for i, example in enumerate(router_result['example_comments'][:2]):
                logger.info(f"Example {i+1}:")
                if isinstance(example, dict):
                    for k, v in example.items():
                        preview = v[:100] + "..." if isinstance(v, str) and len(v) > 100 else v
                        logger.info(f"  {k}: {preview}")
    except Exception as e:
        logger.error(f"Failed to analyze comments with OpenRouter: {e}")
    
    # Step 4: Test the API endpoint directly
    logger.info("\n=== Step 4: Testing API endpoint ===")
    try:
        backend_url = os.environ.get("BACKEND_URL", "http://gleaming-celebration-production-0ae0.up.railway.app:8080")
        api_endpoint = f"{backend_url}/api/youtube/analyze"
        
        logger.info(f"Calling API endpoint: {api_endpoint}")
        logger.info(f"Request data: video_url={video_url}, max_comments={max_comments}")
        
        response = requests.post(
            api_endpoint,
            json={"video_url": video_url, "max_comments": max_comments},
            timeout=60
        )
        
        logger.info(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"API response status: {result.get('status')}")
            logger.info(f"Total comments analyzed: {result.get('total_comments')}")
            
            # Print summary of analysis if successful
            if result.get('status') == 'success' and 'analysis' in result:
                analysis = result['analysis']
                logger.info("Analysis summary:")
                if 'sentiment' in analysis:
                    sentiment = analysis['sentiment']
                    logger.info(f"Sentiment: Positive={sentiment.get('positive_count')}, "
                               f"Neutral={sentiment.get('neutral_count')}, "
                               f"Negative={sentiment.get('negative_count')}")
                
                if 'toxicity' in analysis:
                    toxicity = analysis['toxicity']
                    logger.info(f"Toxicity: {toxicity.get('toxic_count')} toxic comments "
                               f"({toxicity.get('toxic_percentage'):.2f}%)")
        else:
            logger.error(f"API request failed: {response.text}")
    except requests.RequestException as e:
        logger.error(f"Error calling API endpoint: {e}")
        logger.warning("API endpoint might not be running or accessible")
    
    logger.info("\n=== Test completed ===")


if __name__ == "__main__":
    run_test() 