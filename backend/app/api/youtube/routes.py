# app/api/youtube/routes.py
from fastapi import APIRouter, HTTPException, Request
from typing import List, Dict, Any
from pydantic import BaseModel, Field

from .analyzer import extract_video_id, fetch_youtube_comments, analyse_video_comments

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

@router.post(
    "/analyse_full",
    response_model=Dict[str, Any],
    summary="进行完整的YouTube评论分析"
)
async def analyse_full(request: Request, req: YouTubeRequest) -> Dict[str, Any]:
    """
    根据YouTube URL获取评论，分析内容情感和毒性，并用LLM生成回应策略。
    
    处理流程:
    1. 获取YouTube评论
    2. 用NLP模型分析评论情感和毒性
    3. 用LLM生成回应策略和示例
    4. 返回完整的分析结果
    
    Returns:
        Dict包含以下字段:
        - success: 是否成功
        - method: 使用的分析方法
        - duration_s: 处理时间
        - analysis: 包含sentiment、toxicity等分析结果的对象
    """
    result = await analyse_video_comments(request, req.youtube_url, req.limit)
    return result
