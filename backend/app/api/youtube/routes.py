from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
import os

from .analyzer import extract_video_id, fetch_youtube_comments

router = APIRouter(
    prefix="/youtube",
    tags=["youtube"]
)

class YouTubeRequest(BaseModel):
    youtube_url: str = Field(..., description="YouTube 视频链接，例如 https://www.youtube.com/watch?v=... ")
    limit: int = Field(100, description="最多获取的评论数量，最大 100")

@router.post(
    "/analyse",
    response_model=List[str],
    summary="仅返回评论列表"
)
async def get_comments(req: YouTubeRequest):
    """
    返回指定视频的评论列表，仅包含纯文本评论。

    Raises:
        HTTPException 500: YOUTUBE_API_KEY 未配置
        HTTPException 400: 无效的 YouTube URL
        HTTPException 502: 拉取评论时发生错误
    """
    # 检查 API Key
    if not os.getenv("YOUTUBE_API_KEY"):
        raise HTTPException(status_code=500, detail="YOUTUBE_API_KEY 未配置")

    # 提取视频 ID
    video_id = extract_video_id(req.youtube_url)
    if not video_id:
        raise HTTPException(status_code=400, detail="无效的 YouTube URL")

    # 拉取评论
    try:
        comments = fetch_youtube_comments(req.youtube_url, req.limit)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"拉取评论失败: {e}")

    return comments
