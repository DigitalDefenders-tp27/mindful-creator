from typing import List, Dict, Optional
import os, logging, time, traceback

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .analyzer import extract_video_id, fetch_youtube_comments, analyse_comments_with_local_model
from .llm_handler import analyse_youtube_comments

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/youtube",
    tags=["youtube"]
)

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
    criticalComments: List[CriticalCommentResponse]
    success: bool
    message: str = ""

@router.post("/analyse", response_model=List[YouTubeAnalysisResponse])
async def analyse_video(
    yt_req: YouTubeRequest,
    request: Request
):
    start = time.time()
    logger.info(f"Analyse request: url={yt_req.youtube_url}, limit={yt_req.limit}")

    # 确保模型已加载
    if not getattr(request.app.state, "model_loaded", False):
        logger.warning("Model not loaded yet")
        raise HTTPException(status_code=503, detail="Model not loaded")

    # 检查 YouTube API Key
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="YOUTUBE_API_KEY not configured")

    video_id = extract_video_id(yt_req.youtube_url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    # 获取评论
    comments = fetch_youtube_comments(yt_req.youtube_url, yt_req.limit)
    if not comments:
        return [YouTubeAnalysisResponse(
            videoTitle="",
            videoId=video_id,
            thumbnailUrl="",
            totalCommentsAnalysed=0,
            criticalComments=[],
            success=True,
            message="No comments found"
        )]

    # 选择分析方案
    if yt_req.llm_enabled:
        results = analyse_youtube_comments([c['text'] for c in comments]) or []
    else:
        results = analyse_comments_with_local_model([c['text'] for c in comments])

    critical = []
    for r in results:
        orig = next((c for c in comments if c['text']==r.get('comment')), None)
        if orig:
            critical.append(CriticalCommentResponse(
                commentText=orig['text'],
                author=orig['author'],
                publishTime=orig['publishedAt'],
                likesCount=orig['likeCount'],
                responseStrategy=r.get('strategy',''),
                exampleResponse=r.get('example_response','')
            ))

    video_info = {}  # 若需标题及缩略图，可调用 YouTube API 获取

    duration = time.time() - start
    logger.info(f"Analyse completed in {duration:.2f}s, found {len(critical)} critical comments")

    return [YouTubeAnalysisResponse(
        videoTitle=video_info.get('title',''),
        videoId=video_id,
        thumbnailUrl=video_info.get('thumbnail',''),
        totalCommentsAnalysed=len(comments),
        criticalComments=critical,
        success=True
    )]
