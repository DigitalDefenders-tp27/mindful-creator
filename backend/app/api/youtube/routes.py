# app/api/youtube/routes.py
from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel, Field

from .analyzer import extract_video_id, fetch_youtube_comments

router = APIRouter(
    prefix="/youtube",
    tags=["youtube"]
)

class YouTubeRequest(BaseModel):
    youtube_url: str = Field(..., description="完整的 YouTube 视频链接，例如 https://www.youtube.com/watch?v=... ")
    limit: int = Field(100, description="最多获取的评论条数，最大不超过 100")

@router.post(
    "/analyse",
    response_model=List[str],
    summary="仅返回指定视频的评论列表"
)
async def fetch_comments_only(req: YouTubeRequest) -> List[str]:
    """
    根据 Frontend 提供的 YouTube URL 和 limit，获取指定数量的评论文本。
    返回一个字符串列表，每条为一条评论。
    """
    # 提取 video_id
    video_id = extract_video_id(req.youtube_url)
    if not video_id:
        raise HTTPException(status_code=400, detail="无效的 YouTube 视频链接")

    # 获取评论（字符串列表）
    comments = fetch_youtube_comments(req.youtube_url, req.limit)
    if comments is None:
        raise HTTPException(status_code=500, detail="获取评论失败")

    return comments
