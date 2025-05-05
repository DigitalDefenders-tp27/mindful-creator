from typing import List, Optional
import os, logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from googleapiclient.discovery import build

from .analyzer import extract_video_id, get_video_comments

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/youtube", tags=["youtube"])

class YouTubeRequest(BaseModel):
    youtube_url: str
    limit: Optional[int] = Field(100, description="Maximum number of comments to fetch")

@router.post(
    "/analyse",
    response_model=List[str],
    summary="Fetch raw YouTube comments"
)
async def fetch_comments_only(yt_req: YouTubeRequest):
    """
    Only fetch and return the plain text of YouTube comments, no extra metadata.
    """
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        logger.error("YOUTUBE_API_KEY not configured")
        raise HTTPException(status_code=500, detail="YOUTUBE_API_KEY not configured")

    # Extract video ID
    video_id = extract_video_id(yt_req.youtube_url)
    if not video_id:
        logger.error(f"Invalid YouTube URL: {yt_req.youtube_url}")
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    # Fetch comments
    try:
        comments = get_video_comments(
            build('youtube', 'v3', developerKey=api_key),
            video_id,
            yt_req.limit
        )
    except Exception as e:
        logger.error(f"Failed to fetch comments: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch comments")

    # Return only the text of each comment
    return [c["text"] for c in comments]
