import os
import requests
import json
import logging
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build
from gradio_client import Client
import pathlib
import time
import tempfile

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

def fetch_youtube_comments(video_url: str, max_comments: int = 50) -> List[str]:
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

def analyse_comments_with_space_api(comments: List[str]) -> Dict:
    """
    Analyse comments using Space API for sentiment and toxicity
    
    Args:
        comments: List of comments
        
    Returns:
        Analysis results summary
    """
    if not comments:
        logger.warning("No comments available for analysis")
        return {
            "error": "No comments available for analysis"
        }
    
    try:
        # Attempt inference via Hugging Face Space using gradio-client.
        logger.info("Initialising Gradio client for Space inference...")
        cli = Client("Jet-12138/CommentResponse", verbose=False)

        # Call predict with the plain list[str] of comments
        api_start = time.time()
        raw_result: Any = cli.predict(
            comments,                # direct list of comments
            api_name="/predict"
        )
        logger.info("Space call completed in %.2fs", time.time() - api_start)

        # Normalise the result to ensure consistent structure
        space_data = _normalise_space_result(raw_result)

        logger.debug("Normalised payload from Space: %s", space_data)

        # Extract data from normalised result
        sentiment_counts = space_data.get("sentiment_counts", {})
        toxicity_counts = space_data.get("toxicity_counts", {})
        toxicity_total = space_data.get("comments_with_any_toxicity", 0)

        logger.info(
            "Sentiment counts received – positive=%s, neutral=%s, negative=%s",
            sentiment_counts.get("Positive", 0),
            sentiment_counts.get("Neutral", 0),
            sentiment_counts.get("Negative", 0),
        )

        logger.info(
            "Toxicity: %s toxic comments (%.1f%%)",
            toxicity_total,
            (toxicity_total / len(comments) * 100) if comments else 0,
        )

        result = {
            "sentiment": {
                "positive_count": sentiment_counts.get("Positive", 0),
                "neutral_count": sentiment_counts.get("Neutral", 0),
                "negative_count": sentiment_counts.get("Negative", 0)
            },
            "toxicity": {
                "toxic_count": toxicity_total,
                "toxic_percentage": (toxicity_total / len(comments) * 100) if comments else 0,
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
    
    except Exception as ws_err:  # noqa: BLE001 – websocket path failed
        logger.warning(
            "Gradio client websocket path failed (%s); falling back to REST queue "
            "API as a contingency.",
            ws_err,
        )

        try:
            import requests, time as _t
            space_base = "https://jet-12138-commentresponse.hf.space"

            logger.info("Falling back to REST API queue...")
            # 使用标准队列API格式
            logger.info("Pushing task to queue...")
            push_resp = requests.post(
                f"{space_base}/queue/push",
                json={"data": [comments]},  # 使用简单的数据格式
                timeout=60,
            ).json()
            
            # 获取会话哈希
            session_hash = push_resp.get("hash") or push_resp.get("session_hash")
            if not session_hash:
                logger.error(f"Queue response: {push_resp}")
                raise RuntimeError("Space queue/push did not return a session hash")
            
            logger.info(f"Queue task submitted, session hash: {session_hash}")
            
            # 轮询结果
            stream_url = f"{space_base}/queue/data?session_hash={session_hash}"
            space_data = None
            start_time = _t.time()
            
            logger.info("Polling for results...")
            while _t.time() - start_time < 120:  # 最多等待2分钟
                r = requests.get(stream_url, timeout=60)
                if r.status_code != 200:
                    logger.warning(f"Got status code {r.status_code}, retrying...")
                    _t.sleep(2)
                    continue
                    
                response_data = r.json()
                logger.debug(f"Poll response: {str(response_data)[:100]}...")
                
                # 检查是否有data字段且不为空
                arr = response_data.get("data", [])
                if arr and len(arr) > 0 and arr[0]:
                    logger.info("Received result from queue")
                    space_data = _normalise_space_result({"data": arr})
                    break
                    
                # 检查是否任务仍在队列中
                status = response_data.get("status")
                position = response_data.get("queue_position")
                if status:
                    logger.info(f"Task status: {status}, position: {position}")
                
                _t.sleep(2)  # 等待2秒再次轮询
                
            if space_data is None:
                raise RuntimeError("Space queue/data did not return output within timeout")

            # Extract normalised data
            sentiment_counts = space_data.get("sentiment_counts", {})
            toxicity_counts = space_data.get("toxicity_counts", {})
            toxicity_total = space_data.get("comments_with_any_toxicity", 0)
            
            # Return the same structured result as the websocket path
            return {
                "sentiment": {
                    "positive_count": sentiment_counts.get("Positive", 0),
                    "neutral_count": sentiment_counts.get("Neutral", 0),
                    "negative_count": sentiment_counts.get("Negative", 0)
                },
                "toxicity": {
                    "toxic_count": toxicity_total,
                    "toxic_percentage": (toxicity_total / len(comments) * 100) if comments else 0,
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

        except Exception as rest_err:
            logger.error("Fallback REST request also failed: %s", rest_err)
            raise

    except Exception as e:
        logger.error("Space inference failed: %s", e)
        logger.exception("Traceback details:")

        # Fallback – return structured error so that frontend can handle it.
        return {
            "error": "Space inference failed",
            "details": str(e)
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