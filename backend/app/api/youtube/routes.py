# app/api/youtube/routes.py

from typing import List, Dict, Optional
import os, logging, traceback
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .analyzer import extract_video_id, fetch_youtube_comments, analyse_comments_with_local_model
from .llm_handler import analyse_youtube_comments

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/youtube",    # 这里保留 /youtube
    tags=["youtube"]
)

# 请求体定义
class YouTubeRequest(BaseModel):
    youtube_url: str
    limit: Optional[int] = Field(100, description="最大抓取评论数")
    llm_enabled: Optional[bool] = Field(True, description="是否调用 LLM")

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

@router.post(
    "/analyse",
    response_model=List[YouTubeAnalysisResponse],
    summary="分析 YouTube 评论"
)
async def analyse_youtube_video(
    yt_req: YouTubeRequest,
    request: Request
):
    # 1. 模型是否加载
    if not getattr(request.app.state, "model_loaded", False):
        logger.warning("模型尚未加载完成，拒绝请求")
        raise HTTPException(status_code=503, detail="Model not loaded")

    # 2. 检查 API key
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="YOUTUBE_API_KEY 未配置")

    # 3. 解析 video_id
    video_id = extract_video_id(yt_req.youtube_url)
    if not video_id:
        raise HTTPException(status_code=400, detail="无效的 YouTube URL")

    # 4. 调用 YouTube API 拿视频信息和评论
    youtube = build('youtube', 'v3', developerKey=api_key)
    # 简单实现：不再分开 get_video_info/get_video_comments，直接拿评论列表
    comments = fetch_youtube_comments(yt_req.youtube_url, yt_req.limit)

    # 如果没评论，直接返回空
    if not comments:
        return [
            YouTubeAnalysisResponse(
                videoTitle="Unknown",
                videoId=video_id,
                thumbnailUrl="",
                totalCommentsAnalysed=0,
                criticalComments=[],
                success=True,
                message="No comments found"
            )
        ]

    # 5. 分析评论（本地 or LLM）
    comment_texts = [c if isinstance(c, str) else c.get("text","") for c in comments]
    analysis = []
    if yt_req.llm_enabled:
        analysis = analyse_youtube_comments(comment_texts) or []
    else:
        analysis = analyse_comments_with_local_model(comment_texts)

    # 6. 格式化输出
    critical_comments: List[CriticalCommentResponse] = []
    for item in analysis:
        # 如果 LLM 返回的是 {'comment': "...", 'strategy': "...", 'example_response': "..."}
        text = item.get("comment") or item.get("commentText")
        strategy = item.get("strategy") or item.get("responseStrategy")
        example = item.get("example_response") or item.get("exampleResponse")
        # 找原始评论
        idx = comment_texts.index(text) if text in comment_texts else None
        author = comments[idx].get("author","") if idx is not None else ""
        publishedAt = comments[idx].get("publishedAt","") if idx is not None else ""
        likeCount = comments[idx].get("likeCount",0) if idx is not None else 0

        critical_comments.append(
            CriticalCommentResponse(
                commentText=text,
                author=author,
                publishTime=publishedAt,
                likesCount=likeCount,
                responseStrategy=strategy,
                exampleResponse=example
            )
        )

    return [
        YouTubeAnalysisResponse(
            videoTitle="(fetched from API)",   # 这里你可以自己补上真正的视频标题
            videoId=video_id,
            thumbnailUrl="(fetched from API)", # 以及封面 URL
            totalCommentsAnalysed=len(comment_texts),
            criticalComments=critical_comments,
            success=True
        )
    ]