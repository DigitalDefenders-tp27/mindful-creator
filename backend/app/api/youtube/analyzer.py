import os
import requests
import json
import logging
from typing import Dict, List, Any, Optional, Union
from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build
from gradio_client import Client
import pathlib
import time
import tempfile
import sys

# Ensure project root directory is in the Python path
proj_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

# Import LLM handler if available
# Disabled: OpenRouter fallback is disabled as requested
# try:
#     from app.api.youtube.llm_handler import analyse_youtube_comments as llm_analyse_comments
#     HAS_LLM_HANDLER = True
# except ImportError:
#     HAS_LLM_HANDLER = False
#     logging.warning("LLM handler not available, fallback to OpenRouter will not work")

HAS_LLM_HANDLER = False  # Explicitly disable LLM fallback

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Environment variables
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

# Print environment variables for debugging
logger.info(f"YOUTUBE_API_KEY set: {bool(YOUTUBE_API_KEY)}")

# If environment variables are not set, set them manually
if not YOUTUBE_API_KEY:
    YOUTUBE_API_KEY = "AIzaSyDU95gTm6jKz85RdDj84QpU1tUETrCCP8M"
    logger.info(f"Manually set YOUTUBE_API_KEY: {bool(YOUTUBE_API_KEY)}")

def extract_video_id(youtube_url: str) -> str:
    """
    Extract video ID from a YouTube URL
    
    Args:
        youtube_url: YouTube video URL
        
    Returns:
        YouTube video ID
    """
    logger.info(f"Extracting video ID from URL: {youtube_url}")
    
    # Handle different URL formats
    parsed_url = urlparse(youtube_url)
    
    if parsed_url.hostname in ('youtu.be', 'www.youtu.be'):
        # youtu.be/{video_id} format
        video_id = parsed_url.path.strip('/')
        logger.info(f"Extracted video ID from youtu.be short link: {video_id}")
        return video_id
    
    if parsed_url.hostname in ('youtube.com', 'www.youtube.com'):
        # youtube.com/watch?v={video_id} format
        query_params = parse_qs(parsed_url.query)
        video_id = query_params.get('v', [None])[0]
        logger.info(f"Extracted video ID from standard YouTube URL: {video_id}")
        return video_id
    
    # If input is just the video ID
    if youtube_url and len(youtube_url) == 11:
        logger.info(f"Input is already a video ID: {youtube_url}")
        return youtube_url
    
    logger.warning(f"Could not extract video ID from URL: {youtube_url}")
    return None

def fetch_youtube_comments(video_url: str, max_comments: int = 100) -> List[str]:
    """
    Fetch comments from a YouTube video
    
    Args:
        video_url: YouTube video URL
        max_comments: Maximum number of comments to retrieve
        
    Returns:
        List of comments
    """
    video_id = extract_video_id(video_url)
    if not video_id:
        logger.error(f"Could not extract video ID from URL: {video_url}")
        raise ValueError("Could not extract video ID from URL")
    
    logger.info(f"Extracted video ID: {video_id}")
    
    if not YOUTUBE_API_KEY:
        logger.error("YOUTUBE_API_KEY environment variable not set")
        raise ValueError("YOUTUBE_API_KEY environment variable not set")
    
    logger.info("Initialising YouTube API client...")
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    
    comments = []
    next_page_token = None
    
    logger.info(f"Fetching YouTube comments, limit: {max_comments}")
    
    while len(comments) < max_comments:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=min(100, max_comments - len(comments)),
            pageToken=next_page_token,
            textFormat="plainText"
        )
        
        try:
            logger.info(f"Fetching comment batch, currently retrieved: {len(comments)}")
            response = request.execute()
            
            items = response.get("items", [])
            if not items:
                logger.warning("No more comments available")
                break
                
            batch_size = 0
            for item in items:
                comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(comment_text)
                batch_size += 1
            
            logger.info(f"Retrieved {batch_size} comments in this batch")
            
            next_page_token = response.get("nextPageToken")
            if not next_page_token or len(comments) >= max_comments:
                logger.info("No next page token or comment limit reached")
                break
                
        except Exception as e:
            logger.error(f"Error fetching comments: {str(e)}")
            break
    
    logger.info(f"Successfully retrieved {len(comments)} comments")
    
    # Log a few comments as examples
    if comments:
        sample_size = min(3, len(comments))
        logger.debug(f"Comment samples (first {sample_size}):")
        for i in range(sample_size):
            preview = comments[i][:50] + "..." if len(comments[i]) > 50 else comments[i]
            logger.debug(f"  {i+1}. {preview}")
    
    return comments

def _normalise_space_result(result: Any) -> Dict:
    """
    Normalise the result from Space API to always be a dictionary with consistent structure
    
    Args:
        result: The result from Space API (can be string or dict with various structures)
        
    Returns:
        Normalised result with consistent dictionary structure
    """
    logger.debug(f"Normalising Space result type: {type(result)}")
    
    # First convert string to dict if needed
    if isinstance(result, str):
        logger.debug("Decoding JSON string returned by Space...")
        try:
            result = json.loads(result)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON string: {e}")
            raise ValueError(f"Invalid JSON response from Space API: {e}")
    
    # Check if we have a dict now
    if not isinstance(result, dict):
        logger.error(f"Unexpected Space API result format: {type(result)}")
        raise ValueError(f"Unexpected Space API result format: {type(result)}")
    
    # If the result has a "data" field with a list inside (REST API format)
    if "data" in result and isinstance(result["data"], list) and len(result["data"]) > 0:
        logger.debug("Unwrapping data array from REST API response")
        # Extract the first item from the data array (should be our actual result)
        result = result["data"][0]
    
    # Ensure we have the expected keys
    if not any(key in result for key in ["sentiment_counts", "toxicity_counts", "comments_with_any_toxicity"]):
        logger.warning(f"Normalised result may not have expected structure: {list(result.keys())}")
    
    return result

def analyse_comments_with_space_api(comments: List[Any]) -> Dict:
    """
    Analyse comments using Space API for sentiment and toxicity
    
    Args:
        comments: List of comments (should be a list of strings)
        
    Returns:
        Analysis results summary
    """
    if not comments:
        logger.warning("No comments available for analysis")
        return {
            "error": "No comments available for analysis"
        }
    
    # Validate comments format
    if not isinstance(comments, list):
        logger.error("Comments must be a list")
        return {"error": "Comments must be a list"}
        
    # Ensure all comments are strings and limit to 100
    processed_comments = []
    for comment in comments[:100]:
        if isinstance(comment, str) and comment.strip():
            # 移除任何可能的路径对象
            processed_comments.append(str(comment).strip())
        else:
            logger.warning(f"Skipping invalid comment: {comment}")
    
    if not processed_comments:
        logger.warning("No valid comments after filtering")
        return {"error": "No valid comments available for analysis"}
    
    # Calculate total number of comments for percentage calculations
    total_comments = len(processed_comments)
    logger.info(f"Total comments to analyze: {total_comments}")
    
    try:
        # Attempt inference via Hugging Face Space using gradio-client
        logger.info("Initialising Gradio client for Space inference...")
        cli = Client("Jet-12138/CommentResponse", verbose=False)

        # Call predict with comments - gradio-client will handle the wrapping
        api_start = time.time()
        
        # Log what we're sending to the API for debugging
        logger.info(f"Sending {len(processed_comments)} comments to Space API")
        sample_comment = processed_comments[0] if processed_comments else ""
        logger.info(f"Sample comment: {sample_comment[:50]}...")
        
        try:
            # When using gradio-client, directly pass the list of comments
            # The client will handle the wrapping in {"data": [...]} format
            raw_result = cli.predict(
                processed_comments,  # Just pass the list of strings
                api_name="/predict"
            )
            logger.info("Space call completed in %.2fs", time.time() - api_start)
            
            # If we get here, the call succeeded
            # Log the raw result for debugging
            logger.info(f"Raw result type: {type(raw_result)}")
            if isinstance(raw_result, dict):
                logger.info(f"Raw result keys: {list(raw_result.keys())}")
            elif isinstance(raw_result, str):
                logger.info(f"Raw result (first 200 chars): {raw_result[:200]}...")
            else:
                logger.info(f"Raw result format: {raw_result.__class__.__name__}")
            
            # Normalize the result to ensure consistent structure
            space_data = _normalise_space_result(raw_result)
            logger.info(f"Normalized result keys: {list(space_data.keys()) if isinstance(space_data, dict) else 'not a dict'}")
            
            # Extract and log sentiment and toxicity data
            sentiment_counts = space_data.get("sentiment_counts", {})
            logger.info(f"Sentiment counts: {sentiment_counts}")
            
            toxicity_counts = space_data.get("toxicity_counts", {})
            logger.info(f"Toxicity counts: {toxicity_counts}")
            
            toxicity_total = int(space_data.get("comments_with_any_toxicity", 0))
            logger.info(f"Total toxic comments: {toxicity_total}")
        except Exception as e:
            logger.error(f"Space API call failed: {str(e)}")
            
            # If the Space API fails completely, return a standardized error structure 
            # that the frontend can handle
            return {
                "sentiment": {
                    "positive_count": 0,
                    "neutral_count": 0,
                    "negative_count": 0
                },
                "toxicity": {
                    "toxic_count": 0,
                    "toxic_percentage": 0,
                    "toxic_types": {
                        "toxic": 0,
                        "severe_toxic": 0,
                        "obscene": 0,
                        "threat": 0,
                        "insult": 0,
                        "identity_hate": 0
                    }
                },
                "note": f"API Error: {str(e)[:100]}..."
            }

        result = {
            "sentiment": {
                "positive_count": sentiment_counts.get("Positive", 0),
                "neutral_count": sentiment_counts.get("Neutral", 0),
                "negative_count": sentiment_counts.get("Negative", 0)
            },
            "toxicity": {
                "toxic_count": toxicity_total,
                "toxic_percentage": (toxicity_total / total_comments * 100) if total_comments else 0,
                "toxic_types": {
                    "toxic": toxicity_counts.get("Toxic", 0),
                    "severe_toxic": toxicity_counts.get("Severe Toxic", 0),
                    "obscene": toxicity_counts.get("Obscene", 0),
                    "threat": toxicity_counts.get("Threat", 0),
                    "insult": toxicity_counts.get("Insult", 0),
                    "identity_hate": toxicity_counts.get("Identity Hate", 0)
                }
            }
        }

        return result
    
    except Exception as e:
        logger.error(f"Unexpected error in Space API analysis: {str(e)}")
        
        # Always return a consistent structure even on error
        return {
            "sentiment": {
                "positive_count": 0,
                "neutral_count": 0,
                "negative_count": 0
            },
            "toxicity": {
                "toxic_count": 0,
                "toxic_percentage": 0,
                "toxic_types": {
                    "toxic": 0,
                    "severe_toxic": 0,
                    "obscene": 0,
                    "threat": 0,
                    "insult": 0,
                    "identity_hate": 0
                }
            },
            "error": str(e),
            "note": "Analysis failed, please try again or with different comments."
        }

async def analyze_youtube_video(video_url: str) -> Dict:
    """
    Analyse YouTube video comments
    
    Args:
        video_url: YouTube video URL
        
    Returns:
        Analysis results summary
    """
    logger.info(f"Starting YouTube video comment analysis: {video_url}")
    
    try:
        # Fetch YouTube comments
        logger.info("Fetching YouTube comments...")
        comments = fetch_youtube_comments(video_url)
        
        if not comments:
            logger.warning("No comments retrieved, video may have no comments or retrieval failed")
            return {
                "status": "error",
                "message": "Could not fetch comments or video has no comments"
            }
        
        # Analyse comments using Space API
        logger.info(f"Starting Space API analysis of {len(comments)} comments...")
        analysis_result = analyse_comments_with_space_api(comments)
        
        if "error" in analysis_result:
            error_msg = analysis_result["error"]
            logger.error(f"Error analysing comments: {error_msg}")
            return {
                "status": "error",
                "message": error_msg
            }
        
        logger.info("Comment analysis complete, preparing results")
        return {
            "status": "success",
            "total_comments": len(comments),
            "analysis": analysis_result
        }
        
    except Exception as e:
        logger.error(f"Exception occurred while processing request: {str(e)}")
        logger.exception("Detailed exception information:")
        return {
            "status": "error",
            "message": str(e)
        } 