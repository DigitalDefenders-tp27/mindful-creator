import os
import requests
import json
import logging
from typing import Dict, List, Any
from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build
from gradio_client import Client
import time

# Configure logging
# logging.basicConfig(level=logging.INFO, 
#                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Environment variables
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

# Print environment variables for debugging
logger.info(f"YOUTUBE_API_KEY set: {bool(YOUTUBE_API_KEY)}")

# If environment variables are not set, set them manually
if not YOUTUBE_API_KEY:
    YOUTUBE_API_KEY = "AIzaSy…"
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

def fetch_youtube_comments(video_url: str, max_comments: int = 10) -> List[str]:
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
        # We wrap the list[str] in a JSON string to prevent the well-known
        # `PosixPath / list` type error deep inside gradio-client's
        # JSONSerialiser. This keeps the payload fully compatible with the
        # Space's `gr.JSON` input component while looking like a plain string
        # to the serialiser.
        logger.info("Initialising Gradio client for Space inference …")
        cli = Client("Jet-12138/CommentResponse", verbose=False)

        # Call predict with the plain list[str] of comments. The gradio-client
        # SDK handles wrapping this into the appropriate JSON schema (i.e.
        # {"data": [[…]]}) before sending the request. This is now the
        # preferred method per project requirements.
        api_start = time.time()
        raw_result: Any = cli.predict(
            comments,                # direct list of comments
            api_name="/predict"
        )
        logger.info("Space call completed in %.2fs", time.time() - api_start)

        # The Space may reply with either JSON already parsed or a JSON
        # serialised string – cover both cases.
        if isinstance(raw_result, str):
            logger.debug("Decoding JSON string returned by Space …")
            space_data = json.loads(raw_result)
        else:
            space_data = raw_result

        logger.debug("Raw payload from Space: %s", space_data)

        # Expected keys according to Space's README
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
            import requests
            space_base = "https://jet-12138-commentresponse.hf.space"

            queue_resp = requests.post(
                f"{space_base}/call/predict",
                json={"data": [comments]},
                timeout=60,
            ).json()

            event_id = str(queue_resp.get("event_id"))
            if not event_id:
                raise RuntimeError("Space did not return an event_id")

            stream_url = f"{space_base}/call/predict/{event_id}"
            stream = requests.get(stream_url, stream=True, timeout=600)

            for ln in stream.iter_lines(decode_unicode=True):
                if ln.startswith("data:") and "sentiment_counts" in ln:
                    space_data = json.loads(ln.removeprefix("data: "))
                    break
            else:
                raise RuntimeError("Stream ended without final payload")

            sentiment_counts = space_data.get("sentiment_counts", {})
            toxicity_counts = space_data.get("toxicity_counts", {})
            toxicity_total = space_data.get("comments_with_any_toxicity", 0)

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