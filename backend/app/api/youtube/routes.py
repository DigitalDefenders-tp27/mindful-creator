from fastapi import APIRouter, HTTPException, Response, Body
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, HttpUrl
import logging
import traceback
import time
import os
import requests

from app.api.youtube.analyzer import analyze_youtube_video, extract_video_id, fetch_youtube_comments, analyse_comments_with_space_api
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

# Model for Space test request
class SpaceTestRequest(BaseModel):
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
            
        # Perform analysis using the Space API
        # The Space API function now handles both 1D and 2D formats internally
        analysis_result = analyse_comments_with_space_api(comments)
        
        # Perform LLM analysis on the original 1D list
        llm_analysis = analyse_youtube_comments(comments)
        
        return {
            "status": "success",
            "total_comments": len(comments),
            "analysis": analysis_result,
            "strategies": llm_analysis.get("strategies", ""),
            "example_comments": llm_analysis.get("example_comments", [])
        }
        
    except Exception as e:
        return {
            "status": "error",
            "total_comments": 0,
            "message": f"Analysis failed: {str(e)}"
        }

@router.post("/test-spaces")
async def test_spaces_connection(request: SpaceTestRequest):
    """
    Test connection to Spaces API
    
    Args:
        request: Test request with comments
        
    Returns:
        Connection test results
    """
    logger.info(f"Received Spaces connection test request, type: {request.test_type}")
    
    try:
        if request.test_type != "spaces_connection":
            return {
                "status": "error",
                "message": "Invalid test type"
            }
        
        if not request.comments or len(request.comments) == 0:
            request.comments = [
                "This is a test comment. Brilliantly done!",
                "This is another test. Absolutely terrible!"
            ]
        
        logger.info(f"Testing Spaces connection with {len(request.comments)} comments")
        
        # Record environment variables
        env_vars = {
            "GRADIO_CLIENT_TEMP_DIR": os.environ.get("GRADIO_CLIENT_TEMP_DIR", "Not set"),
            "GRADIO_CLIENT_REQUEST_TIMEOUT": os.environ.get("GRADIO_CLIENT_REQUEST_TIMEOUT", "Not set"),
            "HF_TOKEN": "Present" if os.environ.get("HF_TOKEN") else "Not set"
        }
        
        # Test connection timing
        start_time = time.time()
        
        # Try to connect to Spaces using our analysis function
        try:
            # Use our actual analysis function
            result = analyse_comments_with_space_api(request.comments)
            analysis_success = True
            
            # Check if it returned an error
            if "error" in result:
                analysis_success = False
                error_details = result.get("error", "Unknown error")
                logger.error(f"Space analysis returned error: {error_details}")
            
            # Keep track of the used method
            used_method = result.get("note", "Unknown method")
        except Exception as e:
            analysis_success = False
            error_details = str(e)
            used_method = "Failed to connect"
            logger.error(f"Space connection failed: {error_details}")
            logger.error(traceback.format_exc())
            
        # If the function test failed, try direct HTTP request
        if not analysis_success:
            logger.info("Main function test failed, trying direct HTTP request...")
            try:
                # Prepare the Space API URL and test with different endpoints
                space_url = "https://jet-12138-commentresponse.hf.space"
                api_endpoints = ["/api/predict", "/run/predict", "/predict"]
                
                # Combine comments into a string with newlines
                comments_text = "\n".join(request.comments)
                
                # Try each endpoint
                direct_request_success = False
                for endpoint in api_endpoints:
                    api_url = f"{space_url}{endpoint}"
                    logger.info(f"Testing direct HTTP connection to: {api_url}")
                    
                    # Prepare request payload
                    payload = {"data": [comments_text]}
                    headers = {"Content-Type": "application/json"}
                    
                    # Add auth if available
                    hf_token = os.environ.get("HF_TOKEN")
                    if hf_token:
                        headers["Authorization"] = f"Bearer {hf_token}"
                    
                    try:
                        # Send the request
                        response = requests.post(
                            api_url,
                            json=payload,
                            headers=headers,
                            timeout=30
                        )
                        
                        if response.status_code == 200:
                            logger.info(f"Beauty! Direct HTTP request to {endpoint} succeeded!")
                            direct_request_success = True
                            used_method = f"Direct HTTP request to {endpoint}"
                            
                            try:
                                # Parse response for extra info
                                result_data = response.json()
                                if "data" in result_data and isinstance(result_data["data"], list):
                                    result_data = result_data["data"][0]
                                    
                                # Update the result with the direct request data
                                result = result_data
                                analysis_success = True
                                break
                                
                            except Exception as parse_err:
                                logger.warning(f"Could not parse response from {endpoint}: {str(parse_err)}")
                        else:
                            logger.warning(f"Direct HTTP request to {endpoint} failed: {response.status_code}")
                            
                    except Exception as req_err:
                        logger.warning(f"Exception during direct request to {endpoint}: {str(req_err)}")
                
                if not direct_request_success:
                    logger.error("All direct HTTP requests failed")
                
            except ImportError:
                logger.warning("requests library not available")
            except Exception as direct_err:
                logger.error(f"Error during direct HTTP test: {str(direct_err)}")
        
        # Calculate timing
        connect_time = time.time() - start_time
        
        # Return results based on final test status
        if analysis_success:
            return {
                "status": "success",
                "message": "Successfully connected to Spaces",
                "connection_method": used_method,
                "details": {
                    "env_vars": env_vars,
                    "connect_time": connect_time,
                    "result_keys": list(result.keys()) if isinstance(result, dict) else "Not a dict",
                    "sentiment_counts": result.get("sentiment", {}).get("sentiment_counts", None) if isinstance(result, dict) else None
                }
            }
        else:
            # Check if we can connect to the Space home page at all
            try:
                home_response = requests.get("https://jet-12138-commentresponse.hf.space/", timeout=10)
                space_reachable = home_response.status_code < 400
            except:
                space_reachable = False
                
            return {
                "status": "error",
                "message": "Failed to connect to Spaces",
                "error_details": error_details,
                "details": {
                    "env_vars": env_vars,
                    "connect_time": connect_time,
                    "space_homepage_reachable": space_reachable
                }
            }
    
    except Exception as e:
        logger.error(f"Error in test_spaces_connection: {str(e)}")
        logger.error(traceback.format_exc())
        return {
            "status": "error",
            "message": f"Test endpoint error: {str(e)}"
        } 