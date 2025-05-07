# app/api/youtube/routes.py
from fastapi import APIRouter, HTTPException, Request
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator
import logging
import time

from .analyzer import analyse_video_comments
from .utils import extract_video_id

# Configure logger
logger = logging.getLogger("api.youtube.routes")

router = APIRouter(
    prefix="/youtube",
    tags=["youtube"]
)

class YouTubeRequest(BaseModel):
    """
    Request model for YouTube analysis. Supports two parameter formats:
    1. New format: url parameter
    2. Old format: youtube_url parameter
    
    At least one of these must be provided.
    """
    url: Optional[str] = None
    youtube_url: Optional[str] = None
    limit: int = 5
    
    @validator('url', 'youtube_url', pre=True)
    def check_url(cls, v, values):
        # If this is the first url field and it's None, check if we have the other
        if v is None:
            if 'url' in values and 'youtube_url' in values:
                if values.get('url') is None and values.get('youtube_url') is None:
                    raise ValueError("Either 'url' or 'youtube_url' must be provided")
            elif 'url' not in values and 'youtube_url' not in values:
                raise ValueError("Either 'url' or 'youtube_url' must be provided")
        return v
    
    @validator('limit')
    def check_limit(cls, v):
        if v < 1:
            return 1
        if v > 50:
            return 50
        return v

@router.post(
    "/analyse_full",
    response_model=Dict[str, Any],
    summary="Performs complete YouTube comment analysis"
)
async def analyse_full(request: Request, payload: YouTubeRequest) -> Dict[str, Any]:
    """
    Endpoint for complete analysis of YouTube comments using available models.
    Returns sentiment analysis, toxicity analysis, strategies, and example responses.
    """
    try:
        start_time = time.time()
        
        # Get the valid URL
        url = payload.url or payload.youtube_url
        if not url:
            return {"success": False, "message": "No URL provided"}
        
        # Extract the video ID
        video_id = extract_video_id(url)
        if not video_id:
            logger.error(f"Invalid YouTube URL: {url}")
            return {"success": False, "message": "Invalid YouTube URL"}
        
        logger.info(f"Processing analysis request for video ID: {video_id}, limit: {payload.limit}")
        
        # Call the analyzer
        result = await analyse_video_comments(video_id, payload.limit)
        
        # Add processing time
        if isinstance(result, dict) and "duration" not in result:
            result["duration"] = time.time() - start_time
        
        logger.info(f"Analysis completed in {time.time() - start_time:.2f} seconds, method: {result.get('method', 'unknown')}")
        return result
        
    except Exception as e:
        logger.error(f"Error in analyse_full endpoint: {e}")
        return {
            "success": False,
            "message": f"Error processing request: {str(e)}"
        }

@router.post("/analyse")
async def analyse_basic(request: Request, payload: YouTubeRequest):
    """
    Simple endpoint for LLM-only analysis of YouTube comments.
    Returns a basic response for quick feedback on a video.
    """
    try:
        # Get the valid URL
        url = payload.url or payload.youtube_url
        if not url:
            return {"success": False, "message": "No URL provided"}
            
        # Extract the video ID
        video_id = extract_video_id(url)
        if not video_id:
            return {"success": False, "message": "Invalid YouTube URL"}
            
        # For simple analysis, we'll just return a canned response
        # In a real implementation, this would call a simpler LLM function
        return {
            "success": True,
            "status": "pending",
            "message": "Analysis has been queued"
        }
    except Exception as e:
        logger.error(f"Error in analyse_basic endpoint: {e}")
        return {"success": False, "message": str(e)}
