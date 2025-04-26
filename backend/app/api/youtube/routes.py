from fastapi import APIRouter, HTTPException, Body
from typing import Dict
from pydantic import BaseModel, HttpUrl

from app.api.youtube.analyzer import analyze_youtube_video

router = APIRouter()

class YouTubeAnalysisRequest(BaseModel):
    video_url: str
    
    class Config:
        schema_extra = {
            "example": {
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            }
        }

class YouTubeAnalysisResponse(BaseModel):
    status: str
    total_comments: int = 0
    analysis: Dict = {}
    message: str = ""

@router.post("/analyze", response_model=YouTubeAnalysisResponse)
async def analyze_youtube_comments(request: YouTubeAnalysisRequest):
    """
    Analyse YouTube video comments
    
    Receives a YouTube video URL, fetches the video comments, and performs
    sentiment and toxicity analysis using Space API
    
    Returns analysis results including:
    - Positive comments count
    - Neutral comments count
    - Negative comments count
    - Toxic comments count and types (toxicity probability > 30%)
    """
    try:
        result = await analyze_youtube_video(request.video_url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 