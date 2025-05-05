from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from .analyzer import extract_video_id, fetch_youtube_comments

router = APIRouter(
    prefix="/youtube",
    tags=["youtube"]
)

class YouTubeRequest(BaseModel):
    youtube_url: str = Field(..., description="完整的 YouTube 视频链接")
    limit: int = Field(100, description="最多获取多少条评论")

@router.post(
    "/analyse",
    response_model=List[str],
    summary="仅返回评论列表"
)
async def analyse_comments(req: YouTubeRequest):
    """
    只返回指定视频的评论内容列表，按原始顺序。
    """
    video_id = extract_video_id(req.youtube_url)
    if not video_id:
        raise HTTPException(status_code=400, detail="无效的 YouTube URL")

    try:
        comments = fetch_youtube_comments(req.youtube_url, req.limit)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"拉取评论失败：{e}")

    return comments