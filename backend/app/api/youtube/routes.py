from fastapi import APIRouter, HTTPException, Response, Body, status
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, HttpUrl, Field
import logging
import traceback
import time
import os
import requests
from fastapi import BackgroundTasks

from .analyzer import (
    analyse_comments_with_local_model,
    extract_video_id,
    fetch_youtube_comments,
)
from .llm_handler import analyse_youtube_comments

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Add an OPTIONS endpoint to handle preflight CORS requests
@router.options("/analyze")
async def options_analyze():
    """Handle OPTIONS requests for CORS preflight."""
    logger.info("Received OPTIONS request for /analyze endpoint")
    return Response(
        content="",
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Max-Age": "86400",
        }
    )

# Add an OPTIONS endpoint to handle preflight CORS requests for the new endpoint
@router.options("/analyse")
async def options_analyse():
    """Handle OPTIONS requests for CORS preflight."""
    logger.info("Received OPTIONS request for /analyse endpoint")
    return Response(
        content="",
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Max-Age": "86400",
        }
    )

# Add YoutubeRequest model definition
class YoutubeRequest(BaseModel):
    youtube_url: str
    limit: Optional[int] = Field(100, description="Maximum number of comments to fetch")
    llm_enabled: Optional[bool] = Field(True, description="Whether to use LLM for analysis")
    
    class Config:
        schema_extra = {
            "example": {
                "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "limit": 100,
                "llm_enabled": True
            }
        }

class YouTubeAnalysisRequest(BaseModel):
    video_url: str
    max_comments: int = 100  # Default to 20 comments
    
    class Config:
        schema_extra = {
            "example": {
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "max_comments": 100
            }
        }

class YouTubeAnalysisResponse(BaseModel):
    status: str
    total_comments: int
    analysis: Optional[Dict[str, Any]] = None
    strategies: Optional[str] = None
    example_comments: Optional[List[Dict[str, str]]] = None
    message: Optional[str] = None

# Model for test request
class TestRequest(BaseModel):
    test_type: str
    comments: List[str]

@router.post("/analyse")
async def analyse_youtube_comments(
    request: YoutubeRequest,
    background_tasks: BackgroundTasks
):
    """
    Analyse YouTube comments and generate response strategies.
    
    Args:
        request: The YouTube analysis request containing the video URL and other parameters
        background_tasks: FastAPI background tasks
        
    Returns:
        Analysis results
    """
    try:
        # Extract video ID for reference
        video_id = extract_video_id(request.youtube_url)
        if not video_id:
            raise HTTPException(
                status_code=400, 
                detail="Invalid YouTube URL. Could not extract video ID."
            )
            
        # Get comments directly from the URL
        limit = request.limit or 100
        logger.info(f"Extracting comments for video URL: {request.youtube_url} with limit: {limit}")
        
        comments = fetch_youtube_comments(request.youtube_url, limit)
        
        if not comments:
            return {"error": "No comments found for this video"}
        
        # First get basic analysis
        if os.environ.get("MODEL_LOADED", "false").lower() != "true":
            # If model isn't loaded, return a specific message
            basic_analysis = analyse_comments_with_local_model(comments)
            return {
                "video_id": video_id,
                "analysis": basic_analysis,
                "model_status": "not_loaded",
                "message": "NLP model not loaded. Only basic analysis is available."
            }
        
        # If model is loaded, perform both local and LLM analysis
        basic_analysis = analyse_comments_with_local_model(comments)
        
        # Schedule the LLM analysis in the background if needed
        if request.llm_enabled:
            logger.info("Scheduling LLM comment analysis in background")
            background_tasks.add_task(
                analyse_youtube_comments,
                comments
            )
            llm_status = "processing"
        else:
            llm_status = "disabled"
            
        return {
            "video_id": video_id,
            "analysis": basic_analysis,
            "llm_status": llm_status,
            "model_status": "loaded"
        }
            
    except Exception as e:
        logger.error(f"Error in analyse_youtube_comments: {str(e)}")
        logger.exception(e)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze YouTube comments: {str(e)}"
        )

@router.post("/test-model")
async def test_local_model(request: TestRequest):
    """
    Test local NLP model
    
    Args:
        request: Test request with comments
        
    Returns:
        Test results
    """
    logger.info(f"Received local model test request, type: {request.test_type}")
    
    try:
        if request.test_type != "model_test":
            return {
                "status": "error",
                "message": "Invalid test type"
            }
        
        if not request.comments or len(request.comments) == 0:
            request.comments = [
                "This is a test comment. Brilliantly done!",
                "This is another test. Absolutely terrible!"
            ]
        
        logger.info(f"Testing local model with {len(request.comments)} comments")
        
        # Test connection timing
        start_time = time.time()
        
        # Try to analyze with local model
        try:
            # Use our actual analysis function
            result = analyse_comments_with_local_model(request.comments)
            analysis_success = True
            
            # Check if it returned an error
            if "error" in result:
                analysis_success = False
                error_details = result.get("error", "Unknown error")
                logger.error(f"Local model analysis returned error: {error_details}")
            
            # Keep track of the method used
            used_method = result.get("note", "Unknown method")
        except Exception as e:
            analysis_success = False
            error_details = str(e)
            used_method = "Failed to use local model"
            logger.error(f"Local model analysis failed: {error_details}")
            logger.error(traceback.format_exc())
        
        # Calculate timing
        process_time = time.time() - start_time
        
        # Return results based on test status
        if analysis_success:
            return {
                "status": "success",
                "message": "Successfully analyzed with local model",
                "method": used_method,
                "details": {
                    "process_time": process_time,
                    "result_keys": list(result.keys()) if isinstance(result, dict) else "Not a dict",
                    "sentiment": result.get("sentiment", {}),
                    "toxicity": result.get("toxicity", {})
                }
            }
        else:
            return {
                "status": "error",
                "message": "Failed to analyze with local model",
                "error_details": error_details,
                "details": {
                    "process_time": process_time
                }
            }
    
    except Exception as e:
        logger.error(f"Error in test_local_model: {str(e)}")
        logger.error(traceback.format_exc())
        return {
            "status": "error",
            "message": f"Test failed with exception: {str(e)}"
        }

@router.get("/test")
def test_youtube_endpoint():
    """
    Test endpoint for YouTube API
    """
    try:
        return {
            "status": "success",
            "message": "YouTube API endpoint is working"
        }
    except Exception as e:
        logger.error(f"Test endpoint error: {e}")
        return {
            "status": "error",
            "message": f"Test endpoint error: {str(e)}"
        } 