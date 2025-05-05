# app/api/youtube/routes.py
from fastapi import APIRouter, HTTPException, Request
from typing import List, Dict, Any
from pydantic import BaseModel, Field

from .analyzer import extract_video_id, fetch_youtube_comments, analyse_video_comments

router = APIRouter(
    prefix="/youtube",
    tags=["youtube"]
)

class YouTubeRequest(BaseModel):
    youtube_url: str = Field(..., description="Complete YouTube video URL, e.g. https://www.youtube.com/watch?v=... ")
    limit: int = Field(100, description="Maximum number of comments to fetch, up to 100")

@router.post(
    "/analyse",
    response_model=List[str],
    summary="Returns only the comments list for the specified video"
)
async def fetch_comments_only(req: YouTubeRequest) -> List[str]:
    """
    Fetches a specified number of comments based on the YouTube URL and limit provided by the frontend.
    Returns a list of strings, each representing a comment.
    """
    # Extract video_id
    video_id = extract_video_id(req.youtube_url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube video URL")

    # Fetch comments (list of strings)
    comments = fetch_youtube_comments(req.youtube_url, req.limit)
    if comments is None:
        raise HTTPException(status_code=500, detail="Failed to fetch comments")

    return comments

@router.post(
    "/analyse_full",
    response_model=Dict[str, Any],
    summary="Performs complete YouTube comment analysis"
)
async def analyse_full(request: Request, req: YouTubeRequest) -> Dict[str, Any]:
    """
    Retrieves comments based on YouTube URL, analyses sentiment and toxicity, and generates response strategies with LLM.
    
    Processing flow:
    1. Fetch YouTube comments
    2. Analyse comments with NLP model for sentiment and toxicity
    3. Generate response strategies and examples with LLM
    4. Return complete analysis results
    
    Returns:
        Dict containing the following fields:
        - success: Whether the operation was successful
        - method: Analysis method used
        - duration_s: Processing time
        - analysis: Object containing sentiment, toxicity and other analysis results
    """
    result = await analyse_video_comments(request, req.youtube_url, req.limit)
    return result
