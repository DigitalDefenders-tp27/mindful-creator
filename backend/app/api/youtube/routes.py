# app/api/youtube/routes.py

import os
import time
import logging
import traceback
from typing import List, Dict, Any, Optional

from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .analyzer import (
    extract_video_id,
    fetch_youtube_comments,
    analyse_comments_with_local_model,
)
from .llm_handler import analyse_youtube_comments as llm_analyse_comments

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────
# Pydantic 请求/响应模型
# ──────────────────────────────────────────────────────────────
class YouTubeRequest(BaseModel):
    youtube_url: str = Field(..., description="完整的 YouTube 视频 URL")
    limit: Optional[int] = Field(100, description="最多抓取多少条评论")
    llm_enabled: Optional[bool] = Field(True, description="是否启用 LLM 分析")

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

# ──────────────────────────────────────────────────────────────
# 路由定义
# ──────────────────────────────────────────────────────────────
router = APIRouter(
    prefix="/youtube",
    tags=["youtube"],
)


@router.post(
    "/analyse",
    response_model=List[YouTubeAnalysisResponse],
    status_code=status.HTTP_200_OK,
    summary="分析 YouTube 评论",
)
async def analyse_youtube_video(
    yt_req: YouTubeRequest,
    request: Request
) -> List[YouTubeAnalysisResponse]:
    """
    分析 YouTube 视频评论，返回关键评论和回复策略。
    """
    start = time.time()
    logger.info(f"[YouTube] request: url={yt_req.youtube_url}, limit={yt_req.limit}, llm={yt_req.llm_enabled}")

    # 1. 检查本地模型是否加载
    if not getattr(request.app.state, "model_loaded", False):
        logger.warning("本地 NLP 模型尚未加载")
        raise HTTPException(status_code=503, detail="Model not loaded")

    # 2. 抓取评论
    video_id = extract_video_id(yt_req.youtube_url)
    if not video_id:
        logger.error("无法从 URL 中提取 video_id")
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    try:
        comments = fetch_youtube_comments(yt_req.youtube_url, yt_req.limit)
    except Exception as e:
        logger.error(f"fetch_youtube_comments 出错: {e}")
        raise HTTPException(status_code=502, detail="Failed to fetch comments")

    # 3. 如果没评论，直接返回空结果
    if not comments:
        return [
            YouTubeAnalysisResponse(
                videoTitle="",
                videoId=video_id,
                thumbnailUrl="",
                totalCommentsAnalysed=0,
                criticalComments=[],
                success=True,
                message="No comments found"
            )
        ]

    # 4. 依据 llm_enabled 选择分析器
    try:
        if yt_req.llm_enabled:
            # LLM 分析
            comment_texts = [c["text"] for c in comments]
            llm_results = llm_analyse_comments(comment_texts) or []
            analysis_results = llm_results
        else:
            # 本地模型分析
            analysis_results = analyse_comments_with_local_model(comments)
    except Exception as e:
        logger.error(f"评论分析出错: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Analysis error")

    # 5. 将分析结果映射到响应模型
    critical_comments: List[CriticalCommentResponse] = []
    # LLM 返回 list of dicts: { comment, strategy, example_response }
    for item in analysis_results:
        # 找到原始评论
        orig = next((c for c in comments if c["text"] == item.get("comment")), None)
        if not orig:
            continue
        critical_comments.append(
            CriticalCommentResponse(
                commentText=orig["text"],
                author=orig["author"],
                publishTime=orig["publishedAt"],
                likesCount=orig["likeCount"],
                responseStrategy=item.get("strategy", ""),
                exampleResponse=item.get("example_response", "")
            )
        )

    resp = YouTubeAnalysisResponse(
        videoTitle="",     # 如果需要，可以额外通过 API 获取视频 title 和 thumbnail
        videoId=video_id,
        thumbnailUrl="",
        totalCommentsAnalysed=len(comments),
        criticalComments=critical_comments,
        success=True,
        message=""
    )
    logger.info(f"[YouTube] analysis done in {time.time()-start:.2f}s, found {len(critical_comments)} critical comments")
    return [resp]