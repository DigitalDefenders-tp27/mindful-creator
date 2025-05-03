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

@router.post("/analyze", response_model=YouTubeAnalysisResponse, status_code=HTTP_200_OK)
async def analyze_youtube_comments_endpoint(
    request: YouTubeAnalysisRequest
) -> Dict[str, Any]:
    """
    Analyze YouTube comments for a given video URL.
    """
    # Set longer processing timeout - max 5 minutes
    start_time = time.time()
    max_time = 300  # 5 minute timeout
    
    try:
        logger.info(f"Received request to analyze comments from: {request.video_url}")
        
        # Extract video ID and fetch comments
        try:
            logger.info("Extracting video ID")
            video_id = extract_video_id(request.video_url)
            if not video_id:
                logger.error(f"Failed to extract video ID from URL: {request.video_url}")
                return {
                    "success": False,
                    "message": "Could not extract video ID from the provided URL"
                }
            
            logger.info(f"Fetching comments for video ID: {video_id}")
            comments = fetch_youtube_comments(request.video_url, request.max_comments)
            
            if not comments:
                logger.warning(f"No comments found for video ID: {video_id}")
                return {
                    "success": False, 
                    "message": "No comments found for this video. It may have comments disabled or no comments yet."
                }
                
            logger.info(f"Successfully retrieved {len(comments)} comments")
        except Exception as e:
            logger.error(f"Error fetching comments: {str(e)}")
            return {
                "success": False,
                "message": f"Error fetching comments: {str(e)}"
            }
        
        # Create results dictionary to return partial results even if some analysis modules fail
        results = {
            "success": True,
            "video_id": video_id,
            "comment_count": len(comments),
            "sentiment_analysis": None,
            "llm_analysis": None,
            "processing_time_seconds": 0
        }
        
        # Check if we're already out of time
        current_time = time.time()
        remaining_time = max_time - (current_time - start_time)
        logger.info(f"Time used so far: {current_time - start_time:.2f}s, remaining: {remaining_time:.2f}s")
        
        # Analyze comments with local model
        if remaining_time > 10:  # Make sure we have at least 10 seconds to process
            try:
                logger.info("Starting sentiment analysis with local model")
                sentiment_results = analyse_comments_with_local_model(comments)
                results["sentiment_analysis"] = sentiment_results
                logger.info("Sentiment analysis completed successfully")
            except Exception as e:
                logger.error(f"Error in sentiment analysis: {str(e)}")
                # Don't return error, continue processing
        else:
            logger.warning("Skipping sentiment analysis due to time constraints")
        
        # Check remaining time again
        current_time = time.time()
        remaining_time = max_time - (current_time - start_time)
        logger.info(f"Time used after sentiment analysis: {current_time - start_time:.2f}s, remaining: {remaining_time:.2f}s")
        
        # Analyze comments with LLM
        if remaining_time > 10:  # Make sure we have at least 10 seconds to process
            try:
                logger.info("Starting LLM analysis")
                llm_results = analyse_youtube_comments(comments)
                results["llm_analysis"] = llm_results
                logger.info("LLM analysis completed successfully")
            except Exception as e:
                logger.error(f"Error in LLM analysis: {str(e)}")
                # Don't return error, continue processing
        else:
            logger.warning("Skipping LLM analysis due to time constraints")
        
        # Calculate processing time and add to results
        end_time = time.time()
        results["processing_time_seconds"] = round(end_time - start_time, 2)
        logger.info(f"Analysis completed in {results['processing_time_seconds']} seconds")
        
        return results
        
    except Exception as e:
        # Calculate processing time and add to results
        end_time = time.time()
        processing_time = round(end_time - start_time, 2)
        
        logger.error(f"Unhandled error in analyze_youtube_comments_endpoint after {processing_time}s: {str(e)}")
        # Ensure response format is correct
        return {
            "success": False,
            "message": f"An unexpected error occurred: {str(e)}",
            "processing_time_seconds": processing_time
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