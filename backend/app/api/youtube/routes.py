from fastapi import APIRouter, HTTPException, Response, Body
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, HttpUrl
import logging
import traceback
import time
import os
import requests

from app.api.youtube.analyzer import analyze_youtube_video, extract_video_id, fetch_youtube_comments, analyse_comments_with_local_model
from app.api.youtube.llm_handler import analyse_youtube_comments

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class YouTubeAnalysisRequest(BaseModel):
    video_url: str
    max_comments: int = 100  # Default to 20 comments
    
    class Config:
        schema_extra = {
            "example": {
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "max_comments": 10
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

@router.post("/analyze", response_model=YouTubeAnalysisResponse)
async def analyze_youtube_comments_endpoint(request: YouTubeAnalysisRequest) -> Dict[str, Any]:
    """Analyse YouTube comments for sentiment and toxicity and generate response strategies."""
    try:
        # Extract video ID from URL
        video_id = extract_video_id(request.video_url)
        if not video_id:
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")
        
        # Fetch comments from YouTube
        comments = fetch_youtube_comments(request.video_url, request.max_comments)
        
        if not comments:
            return {
                "status": "error",
                "total_comments": 0,
                "message": "No comments found for this video"
            }
            
        # Step 1: Perform sentiment/toxicity analysis using local NLP model
        logger.info(f"Analyzing {len(comments)} comments with local NLP model")
        analysis_result = analyse_comments_with_local_model(comments)
        
        # Step 2: Use OpenRouter for generating response strategies
        logger.info("Generating response strategies with OpenRouter")
        llm_analysis = analyse_youtube_comments(comments)
        
        # Combine the results
        return {
            "status": "success",
            "total_comments": len(comments),
            "analysis": analysis_result,
            "strategies": llm_analysis.get("strategies", ""),
            "example_comments": llm_analysis.get("example_comments", []),
            "note": analysis_result.get("note", "Analysis performed using multiple methods")
        }
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        logger.error(traceback.format_exc())
        return {
            "status": "error",
            "total_comments": 0,
            "message": f"Analysis failed: {str(e)}"
        }

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
            "message": f"Test endpoint error: {str(e)}"
        } 