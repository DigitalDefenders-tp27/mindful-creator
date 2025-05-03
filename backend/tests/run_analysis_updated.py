import os
import sys
import logging
import requests
import json
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ensure the parent directory is in the Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import the necessary modules
from app.api.youtube.analyzer import extract_video_id, fetch_youtube_comments, analyse_comments_with_local_model
from app.api.youtube.llm_handler import analyse_youtube_comments


def get_model_status():
    """Check if the model is loaded"""
    model_loaded = os.environ.get("MODEL_LOADED", "false").lower() == "true"
    logger.info(f"Model loaded status: {model_loaded}")
    return model_loaded


def test_video_info(video_url):
    """Test basic video information retrieval"""
    logger.info(f"Testing video info for: {video_url}")
    
    video_id = extract_video_id(video_url)
    if not video_id:
        logger.error(f"Could not extract video ID from URL: {video_url}")
        return None
    
    logger.info(f"Extracted video ID: {video_id}")
    return video_id


def test_fetch_comments(video_url, limit=20):
    """Test fetching comments from YouTube"""
    logger.info(f"Fetching up to {limit} comments for video URL: {video_url}")
    
    try:
        start_time = time.time()
        comments = fetch_youtube_comments(video_url, limit)
        fetch_time = time.time() - start_time
        
        logger.info(f"Fetched {len(comments)} comments in {fetch_time:.2f} seconds")
        
        # Display a sample of comments
        for i, comment in enumerate(comments[:3]):
            preview = str(comment)[:100] + "..." if len(str(comment)) > 100 else str(comment)
            logger.info(f"Comment {i+1}: {preview}")
        
        return comments
    except Exception as e:
        logger.error(f"Error fetching comments: {e}")
        return None


def test_local_analysis(comments):
    """Test local model analysis"""
    if not comments:
        logger.error("No comments to analyze")
        return None
    
    logger.info(f"Analyzing {len(comments)} comments with local model")
    
    try:
        start_time = time.time()
        result = analyse_comments_with_local_model(comments)
        analysis_time = time.time() - start_time
        
        logger.info(f"Analysis completed in {analysis_time:.2f} seconds")
        
        # Check if the model was loaded
        if "note" in result and "model not loaded" in result["note"].lower():
            logger.warning(f"Note: {result['note']}")
            
        # Log sentiment and toxicity analysis
        if "sentiment" in result:
            sentiment = result["sentiment"]
            pos = sentiment.get("positive_count", 0)
            neu = sentiment.get("neutral_count", 0)
            neg = sentiment.get("negative_count", 0)
            logger.info(f"Sentiment: Positive={pos}, Neutral={neu}, Negative={neg}")
            
        if "toxicity" in result:
            toxicity = result["toxicity"]
            toxic_count = toxicity.get("toxic_count", 0)
            toxic_pct = toxicity.get("toxic_percentage", 0)
            logger.info(f"Toxicity: {toxic_count} toxic comments ({toxic_pct:.1f}%)")
            
            if "toxic_types" in toxicity:
                logger.info(f"Toxic types: {json.dumps(toxicity['toxic_types'], indent=2)}")
        
        return result
    except Exception as e:
        logger.error(f"Error analyzing comments with local model: {e}")
        return None


def test_analyse_endpoint(video_url, limit=20, llm_enabled=True):
    """Test the /analyse API endpoint"""
    backend_url = os.environ.get("BACKEND_URL", "http://localhost:8000")
    api_endpoint = f"{backend_url}/api/youtube/analyse"
    
    payload = {
        "youtube_url": video_url,
        "limit": limit,
        "llm_enabled": llm_enabled
    }
    
    logger.info(f"Testing API endpoint: {api_endpoint}")
    logger.info(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        start_time = time.time()
        response = requests.post(
            api_endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60  # 60 second timeout for LLM processing
        )
        request_time = time.time() - start_time
        
        logger.info(f"API response received in {request_time:.2f} seconds")
        logger.info(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            # Log key information from the response
            logger.info(f"Video ID: {result.get('video_id')}")
            
            if "model_status" in result:
                logger.info(f"Model status: {result['model_status']}")
                
            if "llm_status" in result:
                logger.info(f"LLM status: {result['llm_status']}")
                
            if "message" in result:
                logger.info(f"Message: {result['message']}")
                
            # Log analysis summary if available
            if "analysis" in result:
                analysis = result["analysis"]
                logger.info("Analysis summary:")
                print_analysis_summary(analysis)
                
            return result
        else:
            logger.error(f"API request failed: {response.text}")
            return None
    except requests.RequestException as e:
        logger.error(f"Error calling API endpoint: {e}")
        return None


def print_analysis_summary(analysis):
    """Print a summary of the analysis results"""
    if not analysis:
        logger.warning("No analysis data available")
        return
    
    if "sentiment" in analysis:
        sentiment = analysis["sentiment"]
        pos = sentiment.get("positive_count", 0)
        neu = sentiment.get("neutral_count", 0)
        neg = sentiment.get("negative_count", 0)
        total = pos + neu + neg
        
        if total > 0:
            pos_pct = (pos / total) * 100
            neu_pct = (neu / total) * 100
            neg_pct = (neg / total) * 100
            logger.info(f"Sentiment: Positive={pos} ({pos_pct:.1f}%), "
                        f"Neutral={neu} ({neu_pct:.1f}%), "
                        f"Negative={neg} ({neg_pct:.1f}%)")
    
    if "toxicity" in analysis:
        toxicity = analysis["toxicity"]
        toxic_count = toxicity.get("toxic_count", 0)
        non_toxic = toxicity.get("non_toxic_count", 0)
        total = toxic_count + non_toxic
        
        if total > 0:
            toxic_pct = (toxic_count / total) * 100
            logger.info(f"Toxicity: {toxic_count} toxic comments out of {total} ({toxic_pct:.1f}%)")
            
            if "toxic_types" in toxicity:
                types = toxicity["toxic_types"]
                for ttype, count in types.items():
                    if count > 0:
                        logger.info(f"  - {ttype}: {count}")


def run_complete_test():
    """Run a complete test of the YouTube analysis pipeline"""
    logger.info("=== Starting YouTube Analysis Pipeline Test ===")
    
    # Test parameters
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up
    comment_limit = 20
    
    # Step 1: Check model status
    logger.info("\n=== Step 1: Checking Model Status ===")
    model_loaded = get_model_status()
    
    # Step 2: Check video info
    logger.info("\n=== Step 2: Testing Video Info ===")
    video_id = test_video_info(video_url)
    if not video_id:
        logger.error("Test failed: Could not extract video ID")
        return
    
    # Step 3: Fetch comments
    logger.info("\n=== Step 3: Fetching Comments ===")
    comments = test_fetch_comments(video_url, comment_limit)
    if not comments:
        logger.error("Test failed: Could not fetch comments")
        return
    
    # Step 4: Test local model analysis
    logger.info("\n=== Step 4: Testing Local Model Analysis ===")
    local_result = test_local_analysis(comments)
    if not local_result:
        logger.warning("Local model analysis failed or returned no results")
    
    # Step 5: Test API endpoint (without LLM for faster testing)
    logger.info("\n=== Step 5: Testing API Endpoint (without LLM) ===")
    api_result_no_llm = test_analyse_endpoint(video_url, comment_limit, llm_enabled=False)
    
    # Step 6: Test API endpoint with LLM (if requested)
    include_llm = input("Include LLM test? (y/n, default=n): ").lower() == 'y'
    if include_llm:
        logger.info("\n=== Step 6: Testing API Endpoint with LLM ===")
        api_result_with_llm = test_analyse_endpoint(video_url, comment_limit, llm_enabled=True)
    
    logger.info("\n=== Test Completed ===")
    
    # Print test summary
    logger.info("\n=== Test Summary ===")
    logger.info(f"Model loaded: {model_loaded}")
    logger.info(f"Comments fetched: {len(comments) if comments else 0}")
    logger.info(f"Local analysis successful: {local_result is not None}")
    logger.info(f"API endpoint (no LLM) successful: {api_result_no_llm is not None}")
    if include_llm:
        logger.info(f"API endpoint (with LLM) successful: {api_result_with_llm is not None}")


if __name__ == "__main__":
    run_complete_test() 