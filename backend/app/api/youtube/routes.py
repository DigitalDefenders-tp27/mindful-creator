from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, HttpUrl

from app.api.youtube.analyzer import analyze_youtube_video, extract_video_id, fetch_youtube_comments, analyse_comments_with_space_api
from app.api.youtube.llm_handler import analyse_youtube_comments

router = APIRouter()

class YouTubeAnalysisRequest(BaseModel):
    video_url: str
    max_comments: int = 5  # Default to 20 comments
    
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