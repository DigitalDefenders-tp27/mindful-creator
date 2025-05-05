import os
import time
import logging
import traceback
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse, parse_qs

from fastapi import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .llm_handler import analyse_youtube_comments as _remote_llm_analyse

logger = logging.getLogger("app.api.youtube.analyzer")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


def extract_video_id(youtube_url: str) -> Optional[str]:
    parsed = urlparse(youtube_url)
    host = parsed.hostname or ""
    if host in ("youtu.be", "www.youtu.be"):
        return parsed.path.lstrip("/")
    if host in ("youtube.com", "www.youtube.com"):
        return parse_qs(parsed.query).get("v", [None])[0]
    if youtube_url and len(youtube_url) == 11:
        return youtube_url
    logger.warning(f"Could not extract video ID from URL: {youtube_url}")
    return None


def fetch_youtube_comments(video_id: str, max_comments: int = 100) -> List[str]:
    if not YOUTUBE_API_KEY:
        logger.error("YouTube API key not set")
        return []
    comments: List[str] = []
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        next_page: Optional[str] = None

        while len(comments) < max_comments:
            resp = (
                youtube.commentThreads()
                .list(
                    part="snippet",
                    videoId=video_id,
                    textFormat="plainText",
                    maxResults=min(100, max_comments - len(comments)),
                    pageToken=next_page,
                )
                .execute()
            )
            for item in resp.get("items", []):
                text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(text)
            next_page = resp.get("nextPageToken")
            if not next_page:
                break

    except HttpError as e:
        logger.error(f"YouTube API error: {e}")
    except Exception as e:
        logger.error(f"Error fetching comments: {e}")
    logger.info(f"Fetched {len(comments)} comments for video {video_id}")
    return comments


def fetch_comments_fallback(video_id: str, max_comments: int = 100) -> List[str]:
    logger.warning("Using fallback mock comments")
    mock = [
        "This is a mock comment #1",
        "This is a mock comment #2",
        "This is a mock comment #3",
    ]
    return mock[:max_comments]


def analyse_comments_with_local_model(
    request: Request, comments: List[str]
) -> Dict[str, Any]:
    """
    用本地模型分析评论，必须在 `startup` 时已经把 tokenizer/model 放到 app.state
    """
    model_loaded = getattr(request.app.state, "model_loaded", False)
    if not model_loaded:
        logger.warning("NLP model not loaded in app.state, falling back to limited analysis")
        # 返回一个简易统计
        total = len(comments)
        return {
            "note": "Model not loaded, limited analysis",
            "sentiment": {
                "positive_count": 0,
                "neutral_count": total,
                "negative_count": 0,
            },
            "toxicity": {
                "toxic_count": 0,
                "non_toxic_count": total,
            },
        }

    # 真正走本地模型
    try:
        tokenizer = request.app.state.tokenizer
        model = request.app.state.model
        logger.info(f"Running local model on {len(comments)} comments")
        enc = tokenizer(
            comments,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512,
        )
        # 把 input 转到模型所在设备
        device = next(model.parameters()).device
        enc = {k: v.to(device) for k, v in enc.items()}

        # 下面根据你的 CommentMTLModel 输出做批量推理
        batch_size = 32
        sentiment_counts = {"Negative": 0, "Neutral": 0, "Positive": 0}
        toxicity_counts = {
            "Toxic": 0,
            "Severe Toxic": 0,
            "Obscene": 0,
            "Threat": 0,
            "Insult": 0,
            "Identity Hate": 0,
        }
        toxic_comments = 0

        n = enc["input_ids"].size(0)
        for i in range(0, n, batch_size):
            sl = slice(i, i + batch_size)
            out = model(
                input_ids=enc["input_ids"][sl],
                attention_mask=enc["attention_mask"][sl],
                token_type_ids=enc.get("token_type_ids", None)[sl]
                if "token_type_ids" in enc
                else None,
            )
            # sentiment
            logits = out["sentiment_logits"]
            preds = logits.softmax(dim=-1).argmax(dim=-1).tolist()
            for p in preds:
                sentiment_counts[list(sentiment_counts.keys())[p]] += 1

            # toxicity
            probs = out["toxicity_logits"].sigmoid() > 0.3
            toxic_comments += probs.any(dim=1).sum().item()
            for idx, label in enumerate(toxicity_counts):
                toxicity_counts[label] += int(probs[:, idx].sum().item())

        return {
            "note": "Analysis by local model",
            "sentiment": sentiment_counts,
            "toxicity": {
                "counts": toxicity_counts,
                "total_toxic_comments": toxic_comments,
            },
        }

    except Exception as e:
        logger.error(f"Local model inference error: {e}")
        logger.error(traceback.format_exc())
        # 简易 fallback
        total = len(comments)
        return {
            "note": "Local inference failed, fallback",
            "sentiment": {
                "positive_count": 0,
                "neutral_count": total,
                "negative_count": 0,
            },
            "toxicity": {
                "toxic_count": 0,
                "non_toxic_count": total,
            },
        }


async def analyse_video_comments(
    request: Request, youtube_url: str, max_comments: int = 100
) -> Dict[str, Any]:
    """
    入口函数，在 routes.py 里这样调用：
      @router.post("/analyse")
      async def analyse_endpoint(request: Request, payload: YouTubeRequest):
          return await analyse_video_comments(request, payload.youtube_url, payload.limit)
    """
    logger.info(f"Starting analysis for {youtube_url}")
    start = time.time()

    video_id = extract_video_id(youtube_url)
    if not video_id:
        return {"success": False, "message": "Invalid YouTube URL"}

    comments = fetch_youtube_comments(video_id, max_comments)
    if not comments:
        return {"success": True, "totalComments": 0, "criticalComments": []}

    # 优先用本地模型
    if getattr(request.app.state, "model_loaded", False):
        logger.info("Using local model branch")
        result = analyse_comments_with_local_model(request, comments)
        return {
            "success": True,
            "method": "local_model",
            "duration_s": round(time.time() - start, 2),
            "analysis": result,
        }

    # 否则回退到远程 LLM
    logger.info("Local model not available - falling back to remote LLM")
    try:
        llm_res = await _remote_llm_analyse(comments)
        return {
            "success": True,
            "method": "remote_llm",
            "duration_s": round(time.time() - start, 2),
            "analysis": llm_res,
        }
    except Exception as e:
        logger.error(f"Remote LLM error: {e}")
        logger.error(traceback.format_exc())
        return {"success": False, "message": str(e)}