from fastapi import APIRouter, HTTPException, Response, Body, status
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, HttpUrl, Field
import logging
import traceback
import time
import os
import requests
from fastapi import BackgroundTasks
import re
from fastapi.responses import JSONResponse
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .analyzer import (
    analyse_comments_with_local_model,
    extract_video_id,
    fetch_youtube_comments,
)
from .llm_handler import analyse_youtube_comments

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/youtube",
    tags=["youtube"]
)

# Define request and response models
class YouTubeRequest(BaseModel):
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

class YouTubeComment(BaseModel):
    text: str
    author: str
    publishedAt: str
    likeCount: int

class CriticalCommentResponse(BaseModel):
    commentText: str
    author: str
    publishTime: str
    likesCount: int
    responseStrategy: str
    exampleResponse: str

class YouTubeAnalysisResponse(BaseModel):
    videoTitle: str
    videoId: str
    thumbnailUrl: str
    totalCommentsAnalysed: int
    criticalComments: List[CriticalCommentResponse] = []
    success: bool
    message: str = ""

# Model for test request
class TestRequest(BaseModel):
    test_type: str
    comments: List[str]

@router.post("/analyse", response_model=List[YouTubeAnalysisResponse])
async def analyse_youtube_video(
    request: YouTubeRequest
):
    """
    Analyze YouTube video comments, identify critical comments, and provide response strategies
    
    Args:
        request: Request containing video URL and analysis parameters
        
    Returns:
        List of responses containing analysis results
    """
    start_time = time.time()
    logger.info(f"YouTube comment analysis request received: urls={request.youtube_url}, max_comments={request.limit}")
    
    try:
        # Check YouTube API environment variable
        api_key = os.environ.get('YOUTUBE_API_KEY')
        if not api_key:
            logger.error("YouTube API key not found in environment variables")
            return JSONResponse(
                status_code=500,
                content={
                    "success": False, 
                    "message": "YouTube API key not configured"
                }
            )
        
        logger.info("YouTube API key found")
        responses = []
        
        # Extract video ID from request
        video_id = extract_video_id(request.youtube_url)
        if not video_id:
            logger.error("No valid YouTube video ID found in the provided URL")
            return JSONResponse(
                status_code=400,
                content={
                    "success": False, 
                    "message": "No valid YouTube video ID found in the provided URL"
                }
            )
        
        # Build YouTube API client
        youtube = build('youtube', 'v3', developerKey=api_key)
        logger.info(f"YouTube API client built successfully")
        
        # Get video details
        video_info = get_video_info(youtube, video_id)
        logger.info(f"Retrieved video info: title='{video_info['title']}', id={video_id}")
        
        # Get comments
        logger.info(f"Fetching comments for video ID: {video_id}, max_comments: {request.limit}")
        comments_time_start = time.time()
        comments = get_video_comments(youtube, video_id, request.limit)
        comments_time = time.time() - comments_time_start
        logger.info(f"Retrieved {len(comments)} comments in {comments_time:.2f} seconds")
        
        if not comments:
            logger.warning(f"No comments found for video ID: {video_id}")
            responses.append(
                YouTubeAnalysisResponse(
                    videoTitle=video_info["title"],
                    videoId=video_id,
                    thumbnailUrl=video_info["thumbnail"],
                    totalCommentsAnalysed=0,
                    criticalComments=[],
                    success=True,
                    message="No comments found for this video"
                )
            )
            return responses
        
        # Record analysis start
        analysis_time_start = time.time()
        logger.info(f"Starting comment analysis for {len(comments)} comments")
        
        # Use LLM to analyze comments
        model_status = os.environ.get("MODEL_LOADED", "false").lower() == "true"
        if model_status:
            logger.info("Using full LLM analysis")
        else:
            logger.warning("Model not loaded, using simplified analysis")
        
        # Perform comment analysis
        try:
            # Convert comment format
            comment_texts = [comment['text'] for comment in comments]
            logger.info(f"Analyzing {len(comment_texts)} comments using LLM")
            
            # Call LLM analysis function
            analysis_result = analyse_youtube_comments(comment_texts)
            
            if not analysis_result:
                logger.warning("LLM analysis returned no results")
                analysis_result = []
            
            logger.info(f"LLM analysis completed, identified {len(analysis_result)} critical comments")
            
            # Match analysis results with original comments
            critical_comments = []
            for critical_comment in analysis_result:
                # Find the complete information of the original comment
                original_comment = next(
                    (c for c in comments if c['text'] == critical_comment['comment']), 
                    None
                )
                
                if original_comment:
                    critical_comments.append(
                        CriticalCommentResponse(
                            commentText=original_comment['text'],
                            author=original_comment['author'],
                            publishTime=original_comment['publishedAt'],
                            likesCount=original_comment['likeCount'],
                            responseStrategy=critical_comment['strategy'],
                            exampleResponse=critical_comment['example_response']
                        )
                    )
                else:
                    logger.warning(f"Could not find original comment for analysis result: {critical_comment['comment'][:50]}...")
            
            analysis_time = time.time() - analysis_time_start
            logger.info(f"Comment analysis completed in {analysis_time:.2f} seconds")
            
            # Create and add response
            response = YouTubeAnalysisResponse(
                videoTitle=video_info["title"],
                videoId=video_id,
                thumbnailUrl=video_info["thumbnail"],
                totalCommentsAnalysed=len(comments),
                criticalComments=critical_comments,
                success=True
            )
            responses.append(response)
            
        except Exception as e:
            logger.error(f"Error during comment analysis: {str(e)}")
            logger.error(traceback.format_exc())
            responses.append(
                YouTubeAnalysisResponse(
                    videoTitle=video_info["title"],
                    videoId=video_id,
                    thumbnailUrl=video_info["thumbnail"],
                    totalCommentsAnalysed=len(comments),
                    criticalComments=[],
                    success=False,
                    message=f"Error during comment analysis: {str(e)}"
                )
            )
        
        total_time = time.time() - start_time
        logger.info(f"YouTube analysis completed in {total_time:.2f} seconds, processed 1 video")
        return responses
    
    except Exception as e:
        logger.error(f"Unhandled exception in YouTube analysis: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500, 
            detail=f"An unexpected error occurred: {str(e)}"
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

def get_video_info(youtube, video_id: str) -> Dict:
    """Get video details information"""
    try:
        response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()
        
        if not response.get('items'):
            logger.warning(f"No video details found for ID: {video_id}")
            return {
                "title": "Unknown Video",
                "thumbnail": ""
            }
        
        video_data = response['items'][0]['snippet']
        title = video_data.get('title', 'Unknown Video')
        thumbnail = video_data.get('thumbnails', {}).get('high', {}).get('url', '')
        
        logger.info(f"Retrieved video info for ID {video_id}: title='{title}'")
        return {
            "title": title,
            "thumbnail": thumbnail
        }
    except Exception as e:
        logger.error(f"Error getting video info for ID {video_id}: {str(e)}")
        logger.error(traceback.format_exc())
        return {
            "title": "Unknown Video",
            "thumbnail": ""
        }

def get_video_comments(youtube, video_id: str, max_comments: int) -> List[Dict]:
    """Get video comments"""
    try:
        comments = []
        next_page_token = None
        
        while len(comments) < max_comments:
            # Call YouTube API to get comments
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=min(100, max_comments - len(comments)),  # Maximum 100 comments per page
                pageToken=next_page_token
            ).execute()
            
            # Process response data
            for item in response.get('items', []):
                snippet = item.get('snippet', {}).get('topLevelComment', {}).get('snippet', {})
                comment = {
                    'text': snippet.get('textDisplay', ''),
                    'author': snippet.get('authorDisplayName', 'Anonymous'),
                    'publishedAt': snippet.get('publishedAt', ''),
                    'likeCount': snippet.get('likeCount', 0)
                }
                comments.append(comment)
            
            # Check if there is a next page
            next_page_token = response.get('nextPageToken')
            if not next_page_token or len(response.get('items', [])) == 0:
                break
        
        logger.info(f"Retrieved {len(comments)} comments for video ID: {video_id}")
        return comments
    
    except HttpError as e:
        logger.error(f"YouTube API error getting comments for video {video_id}: {str(e)}")
        logger.error(traceback.format_exc())
        if "commentsDisabled" in str(e):
            logger.warning(f"Comments are disabled for video ID: {video_id}")
        return []
    
    except Exception as e:
        logger.error(f"Error getting comments for video {video_id}: {str(e)}")
        logger.error(traceback.format_exc())
        return [] 