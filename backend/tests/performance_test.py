import os
import sys
import logging
import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ensure the parent directory is in the Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from app.api.youtube.analyzer import fetch_youtube_comments, analyse_comments_with_local_model
from app.api.youtube.llm_handler import analyse_youtube_comments


class Timer:
    """Simple timer context manager for measuring execution time"""
    
    def __init__(self, name):
        self.name = name
        self.start_time = None
        self.end_time = None
        self.elapsed = None
    
    def __enter__(self):
        self.start_time = time.time()
        logger.info(f"Starting {self.name} at {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        self.elapsed = self.end_time - self.start_time
        logger.info(f"Completed {self.name} in {self.elapsed:.3f} seconds")
        return False


def run_performance_test():
    """
    Run a performance test on the YouTube comment analysis pipeline,
    measuring the time taken for each step in the process.
    """
    # Test parameters
    video_url = "https://www.youtube.com/watch?v=SS_XY4SosUU"  # Specified YouTube video
    max_comments = 100  # Fetch 100 comments as requested
    
    logger.info("=" * 80)
    logger.info(f"PERFORMANCE TEST STARTED AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Testing with video URL: {video_url}")
    logger.info(f"Comment limit: {max_comments}")
    logger.info("=" * 80)
    
    performance_results = {
        "fetch_comments": None,
        "local_nlp_analysis": None,
        "openrouter_analysis": None,
        "api_endpoint": None,
        "total_time": None,
        "comment_count": 0,
        "start_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "video_url": video_url
    }
    
    start_time = time.time()
    comments = []
    
    # Step 1: Test fetching YouTube comments
    with Timer("YouTube comment fetching") as timer:
        try:
            comments = fetch_youtube_comments(video_url, max_comments)
            logger.info(f"Successfully fetched {len(comments)} comments")
            performance_results["comment_count"] = len(comments)
            
            # Log a sample of comments
            for i, comment in enumerate(comments[:3]):
                preview = comment[:80] + "..." if len(comment) > 80 else comment
                logger.info(f"Sample comment {i+1}: {preview}")
                
        except Exception as e:
            logger.error(f"Failed to fetch YouTube comments: {e}")
            import traceback
            logger.error(traceback.format_exc())
    
    performance_results["fetch_comments"] = timer.elapsed
    
    if not comments:
        logger.error("No comments fetched, cannot continue performance test")
        performance_results["total_time"] = time.time() - start_time
        return performance_results
    
    # Step 2: Test local NLP model
    with Timer("Local NLP model analysis") as timer:
        try:
            local_result = analyse_comments_with_local_model(comments)
            logger.info("Local NLP model analysis summary:")
            
            # Extract and log sentiment statistics
            sentiment = local_result.get("sentiment", {})
            logger.info(f"Sentiment: Positive={sentiment.get('positive_count', 0)}, "
                       f"Neutral={sentiment.get('neutral_count', 0)}, "
                       f"Negative={sentiment.get('negative_count', 0)}")
            
            # Extract and log toxicity statistics
            toxicity = local_result.get("toxicity", {})
            logger.info(f"Toxicity: {toxicity.get('toxic_count', 0)} toxic comments "
                       f"({toxicity.get('toxic_percentage', 0):.2f}%)")
            
        except Exception as e:
            logger.error(f"Failed to analyze comments with local NLP model: {e}")
            import traceback
            logger.error(traceback.format_exc())
    
    performance_results["local_nlp_analysis"] = timer.elapsed
    
    # Step 3: Test OpenRouter analysis
    with Timer("OpenRouter analysis") as timer:
        try:
            router_result = analyse_youtube_comments(comments)
            logger.info(f"OpenRouter analysis status: {router_result.get('status', 'unknown')}")
            
            # Log sample of strategies if available
            if router_result.get("strategies"):
                strategies = router_result["strategies"]
                sample = strategies[:150] + "..." if len(strategies) > 150 else strategies
                logger.info(f"Sample strategies: {sample}")
            
            # Log number of example comments if available
            if router_result.get("example_comments"):
                logger.info(f"Number of example comments: {len(router_result['example_comments'])}")
                
        except Exception as e:
            logger.error(f"Failed to analyze comments with OpenRouter: {e}")
            import traceback
            logger.error(traceback.format_exc())
    
    performance_results["openrouter_analysis"] = timer.elapsed
    
    # Step 4: Test the complete API endpoint
    with Timer("API endpoint complete analysis") as timer:
        try:
            backend_url = os.environ.get("BACKEND_URL", "http://gleaming-celebration-production-0ae0.up.railway.app:8080")
            api_endpoint = f"{backend_url}/api/youtube/analyze"
            
            logger.info(f"Calling API endpoint: {api_endpoint}")
            response = requests.post(
                api_endpoint,
                json={"video_url": video_url, "max_comments": max_comments},
                timeout=120  # Allow up to 2 minutes for the complete analysis
            )
            
            logger.info(f"API response status code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"API response status: {result.get('status', 'unknown')}")
                logger.info(f"Total comments analyzed via API: {result.get('total_comments', 0)}")
            else:
                logger.error(f"API request failed with status code {response.status_code}")
                logger.error(f"Error response: {response.text}")
                
        except Exception as e:
            logger.error(f"Error calling API endpoint: {e}")
            import traceback
            logger.error(traceback.format_exc())
    
    performance_results["api_endpoint"] = timer.elapsed
    
    # Calculate total time
    end_time = time.time()
    total_time = end_time - start_time
    performance_results["total_time"] = total_time
    
    # Output summary
    logger.info("=" * 80)
    logger.info("PERFORMANCE TEST SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Video URL: {video_url}")
    logger.info(f"Comments processed: {performance_results['comment_count']}")
    logger.info(f"Time to fetch {performance_results['comment_count']} comments: {performance_results['fetch_comments']:.3f} seconds")
    logger.info(f"Time for local NLP analysis: {performance_results['local_nlp_analysis']:.3f} seconds")
    logger.info(f"Time for OpenRouter analysis: {performance_results['openrouter_analysis']:.3f} seconds")
    logger.info(f"Time for complete API endpoint call: {performance_results['api_endpoint']:.3f} seconds")
    logger.info(f"Total test time: {total_time:.3f} seconds")
    logger.info("=" * 80)
    
    # Save results to a JSON file
    results_dir = os.path.join(parent_dir, "tests", "results")
    os.makedirs(results_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_file = os.path.join(results_dir, f"performance_test_{timestamp}.json")
    
    with open(result_file, "w") as f:
        json.dump(performance_results, f, indent=2)
    
    logger.info(f"Performance results saved to {result_file}")
    
    return performance_results


if __name__ == "__main__":
    run_performance_test() 