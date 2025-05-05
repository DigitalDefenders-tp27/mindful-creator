from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

from .analyzer import fetch_youtube_comments, extract_video_id

router = APIRouter(
    prefix="/youtube",
    tags=["youtube"],
)

class YouTubeRequest(BaseModel):
    youtube_url: str = Field(..., description="完整的 YouTube 视频链接 或 视频 ID，例如：https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    limit: int = Field(100, description="要拉取的评论数量，最大不超过 100")

@router.post(
    "/analyse",
    response_model=List[str],
    summary="获取 YouTube 评论列表",
    description="仅返回原始评论文本的列表，不包含其他元数据或分析结果。"
)
async def analyse(yt_req: YouTubeRequest):
    """
    接收一个 JSON:
      {
        "youtube_url": "...",
        "limit": 5
      }
    返回一个字符串数组，包含拉取到的评论文本。
    """
    # 验证并提取视频 ID
    video_id = extract_video_id(yt_req.youtube_url)
    if not video_id:
        raise HTTPException(status_code=400, detail="无效的 YouTube 链接或视频 ID")

    # 获取评论
    comments = fetch_youtube_comments(yt_req.youtube_url, yt_req.limit)

    # 如果拉取失败或无评论，直接返回空列表
    return comments
