# app/api/youtube/routes.py
from fastapi import APIRouter, HTTPException, Request
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator
import logging

from .analyzer import extract_video_id, fetch_youtube_comments, Analyzer

# 设置日志记录器
logger = logging.getLogger("api.youtube.routes")

router = APIRouter(
    prefix="/youtube",
    tags=["youtube"]
)

# 创建Analyzer实例
analyzer = Analyzer()

class YouTubeRequest(BaseModel):
    """
    请求模型，支持新旧两种参数格式:
    - 新格式: url, limit
    - 旧格式: youtube_url, limit
    """
    url: Optional[str] = Field(None, description="Complete YouTube video URL (新格式)")
    youtube_url: Optional[str] = Field(None, description="Complete YouTube video URL (旧格式)")
    limit: int = Field(5, description="Maximum number of comments to fetch and analyze")
    
    # 验证器确保至少有一个URL字段被设置
    @validator('youtube_url', 'url', pre=True, always=True)
    def check_url(cls, v, values):
        # 确保至少有一个URL字段有值
        if 'url' in values and values['url'] is not None:
            return v
        if 'youtube_url' in values and values['youtube_url'] is not None:
            return v
        if v is None:
            raise ValueError('Either url or youtube_url must be provided')
        return v

class SingleCommentRequest(BaseModel):
    comment: str = Field(..., description="YouTube comment to analyze")

@router.post(
    "/analyse",
    response_model=Dict[str, Any],
    summary="Analyzes a single comment using the OpenRouter LLM"
)
async def analyse_single_comment(req: SingleCommentRequest) -> Dict[str, Any]:
    """
    Analyzes a single comment and returns a suggested response.
    Uses only the OpenRouter LLM for analysis.
    """
    response = analyzer.analyze_single_comment(req.comment)
    return {"success": True, "response": response}

@router.post(
    "/analyse_full",
    response_model=Dict[str, Any],
    summary="Performs complete YouTube comment analysis"
)
async def analyse_full(req: YouTubeRequest) -> Dict[str, Any]:
    """
    Retrieves comments based on YouTube URL, analyses sentiment and toxicity, and generates response strategies with LLM.
    
    Processing flow:
    1. Fetch YouTube comments
    2. Analyse comments with NLP model for sentiment and toxicity
    3. Generate response strategies and examples with LLM
    4. Return complete analysis results
    
    Returns:
        Dict containing the following fields:
        - success: Whether the operation was successful
        - method: Analysis method used
        - duration: Processing time in seconds
        - nlp_analysis: Results from the NLP model (sentiment, toxicity)
        - llm_analysis: Results from the LLM model
        - strategies: Suggested response strategies
        - example_comments: Example comments with suggested responses
    """
    # 获取有效的URL (优先使用新格式)
    video_url = req.url if req.url is not None else req.youtube_url
    
    logger.info(f"Analyzing YouTube video: {video_url} with limit {req.limit}")
    result = analyzer.analyse_video_comments(video_url, req.limit)
    
    # 为了保持与旧版API兼容，调整一下结果结构
    if "duration" in result:
        result["duration_s"] = result["duration"]
    
    logger.info(f"Analysis completed with method: {result.get('method', 'unknown')}")
    return result
