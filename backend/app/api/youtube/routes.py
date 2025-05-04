from typing import List, Dict, Optional
import logging, time, os, traceback

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .analyzer import (
    analyse_comments_with_local_model,
    extract_video_id,
    fetch_youtube_comments,  
)
from .llm_handler import analyse_youtube_comments

logger = logging.getLogger(__name__)

# ------------------ 路由实例 ------------------
router = APIRouter(
    prefix="/youtube",
    tags=["youtube"]
)

# ------------------ Pydantic 模型 ------------------
class YouTubeRequest(BaseModel):
    youtube_url: str
    limit: Optional[int] = Field(100, description="Maximum number of comments to fetch")
    llm_enabled: Optional[bool] = Field(True, description="Whether to use LLM for analysis")

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

# ------------------ 业务端点 ------------------
@router.post(
    "/analyse",              # ⬅️ 与前端保持一致
    response_model=List[YouTubeAnalysisResponse]
)
async def analyse_youtube_video(
    yt_req: YouTubeRequest,  # ⬅️ 避免与 FastAPI Request 混淆
    request: Request         # ⬅️ 注入 FastAPI Request 以便取模型
):
    start_time = time.time()
    logger.info(
        f"Analyse request: url={yt_req.youtube_url}, limit={yt_req.limit}"
    )

    # ---------- 检查模型 ----------
    if not getattr(request.app.state, "model_loaded", False):
        logger.warning("Model not loaded yet")
        raise HTTPException(status_code=503, detail="Model not loaded")

    tokenizer = request.app.state.tokenizer
    model     = request.app.state.model

    # ---------- 检查 YouTube API ----------
    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="YOUTUBE_API_KEY not configured")

    video_id = extract_video_id(yt_req.youtube_url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    # ---------- 调用 YouTube API ----------
    youtube = build('youtube', 'v3', developerKey=api_key)
    video_info = get_video_info(youtube, video_id)
    comments   = get_video_comments(youtube, video_id, yt_req.limit)

    if not comments:
        return [YouTubeAnalysisResponse(
            videoTitle=video_info["title"],
            videoId=video_id,
            thumbnailUrl=video_info["thumbnail"],
            totalCommentsAnalysed=0,
            criticalComments=[],
            success=True,
            message="No comments found"
        )]

    # ---------- 调用 LLM ----------
    comment_texts = [c["text"] for c in comments]
    analysis = analyse_youtube_comments(comment_texts) or []

    critical_comments: List[CriticalCommentResponse] = []
    for item in analysis:
        orig = next((c for c in comments if c["text"] == item["comment"]), None)
        if orig:
            critical_comments.append(CriticalCommentResponse(
                commentText=orig["text"],
                author=orig["author"],
                publishTime=orig["publishedAt"],
                likesCount=orig["likeCount"],
                responseStrategy=item["strategy"],
                exampleResponse=item["example_response"]
            ))

    return [YouTubeAnalysisResponse(
        videoTitle=video_info["title"],
        videoId=video_id,
        thumbnailUrl=video_info["thumbnail"],
        totalCommentsAnalysed=len(comments),
        criticalComments=critical_comments,
        success=True
    )]


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