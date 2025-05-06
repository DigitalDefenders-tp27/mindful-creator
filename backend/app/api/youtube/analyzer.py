import os
import time
import logging
import traceback
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse, parse_qs
import concurrent.futures
import httpx
import asyncio

from fastapi import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .llm_handler import analyse_youtube_comments as _remote_llm_analyse
from app.api.models.bert_model import BERTModel
from app.api.openai.ai_client import OpenAIClient
from app.api.youtube.client import YouTubeClient
from app.api.utils.logger import setup_logger
from app.api.openrouter.client import OpenRouterClient

logger = setup_logger('analyzer')

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


def extract_video_id(youtube_url: str) -> Optional[str]:
    """
    Extract video ID from YouTube URL
    Supports formats:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - VIDEO_ID (directly as 11-character ID)
    """
    if not youtube_url:
        logger.warning("Empty YouTube URL provided")
        return None
        
    try:
        parsed = urlparse(youtube_url)
        
        # youtu.be format links
        if parsed.hostname in ["youtu.be", "www.youtu.be"]:
            return parsed.path.lstrip("/")
            
        # youtube.com format links
        if parsed.hostname in ["youtube.com", "www.youtube.com"]:
            query_params = parse_qs(parsed.query)
            if "v" in query_params:
                return query_params["v"][0]
                
        # If input looks like already a video ID (11 characters)
        if len(youtube_url) == 11 and "/" not in youtube_url and "?" not in youtube_url:
            return youtube_url
    
        logger.warning(f"Could not extract video ID from URL: {youtube_url}")
        return None
    except Exception as e:
        logger.error(f"Error extracting video ID from {youtube_url}: {str(e)}")
        return None


def fetch_youtube_comments(youtube_url: str, max_comments: int = 100) -> List[str]:
    """
    Fetch YouTube video comments
    
    Args:
        youtube_url: YouTube video URL or video ID
        max_comments: Maximum number of comments to fetch
        
    Returns:
        List of comment texts
    """
    if not YOUTUBE_API_KEY:
        logger.error("YouTube API key not set")
        return []
        
    # Ensure we extract video ID from URL
    video_id = extract_video_id(youtube_url)
    if not video_id:
        logger.error(f"Could not extract video ID from {youtube_url}")
        return []
        
    logger.info(f"Fetching comments for video ID: {video_id}")
    
    comments = []
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        next_page = None

        while len(comments) < max_comments:
            resp = (
                youtube.commentThreads()
                .list(
                    part="snippet",
                    videoId=video_id,  # Use extracted video ID
                    textFormat="plainText",
                    maxResults=min(100, max_comments - len(comments)),
                    pageToken=next_page,
                )
                .execute()
            )
                
            # Extract comment text
            for item in resp.get("items", []):
                text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(text)
                
            # Check if there's another page
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
    Analyse comments with local model, the tokenizer/model must be placed in app.state during startup
    """
    model_loaded = getattr(request.app.state, "model_loaded", False)
    if not model_loaded:
        logger.warning("NLP model not loaded in app.state, falling back to limited analysis")
        # Return a simple count
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

    # Actually use the local model
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
        # Transfer input to the device where model is located
        device = next(model.parameters()).device
        enc = {k: v.to(device) for k, v in enc.items()}

        # Batch inference based on your CommentMTLModel output
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
        # Simple fallback
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
    Entry function, called in routes.py like this:
      @router.post("/analyse")
      async def analyse_endpoint(request: Request, payload: YouTubeRequest):
          return await analyse_video_comments(request, payload.youtube_url, payload.limit)
    """
    logger.info(f"Starting analysis for {youtube_url}")
    start = time.time()

    video_id = extract_video_id(youtube_url)
    if not video_id:
        return {"success": False, "message": "Invalid YouTube URL"}

    comments = fetch_youtube_comments(youtube_url, max_comments)
    if not comments:
        return {"success": True, "totalComments": 0, "criticalComments": []}

    # Default example responses (ensure we have content)
    default_examples = [
        {
            "comment": "This video was so helpful, I learned a lot!",
            "response": "Thanks for the kind words! Really glad you found it helpful."
        },
        {
            "comment": "I don't agree with what you said about this topic.",
            "response": "Thanks for your perspective. I value different viewpoints and appreciate you sharing yours!"
        },
        {
            "comment": "You're completely wrong about this. You should do more research before making videos.",
            "response": "I appreciate your feedback. I do research thoroughly, but I'm always open to learning more. Feel free to share specific resources."
        }
    ]

    # 创建最终返回值容器
    response = {
        "success": True,
        "duration_s": 0,  # 稍后更新
        "nlp_analysis": None,
        "llm_analysis": None,
        "strategies": "",
        "example_comments": []
    }

    # 记录NLP和LLM处理开始时间，用于计算处理耗时
    nlp_start = time.time()
    llm_start = time.time()
    
    # 创建两个任务分别处理NLP和LLM分析，并行执行
    nlp_result = None
    llm_result = None
    
    # 如果本地NLP模型可用，则使用本地模型进行分析
    if getattr(request.app.state, "model_loaded", False):
        logger.info("Using local NLP model for sentiment/toxicity analysis")
        nlp_result = analyse_comments_with_local_model(request, comments)
        logger.info(f"NLP analysis completed in {round(time.time() - nlp_start, 2)}s")
        response["nlp_analysis"] = nlp_result
    else:
        logger.info("Local NLP model not available")
    
    # 始终使用LLM（优先使用OpenRouter）进行策略和示例回复生成
    try:
        logger.info("Calling LLM (OpenRouter) for strategies and examples")
        llm_res = await _remote_llm_analyse(comments)
        
        # 提取策略和示例评论
        strategies = llm_res.get("strategies", "")
        example_comments = llm_res.get("example_comments", [])
        
        logger.info(f"LLM returned {len(example_comments)} example comments")
        
        # 确保我们有示例评论
        if not example_comments or len(example_comments) == 0:
            logger.warning("No example comments from LLM, using defaults")
            example_comments = default_examples
            
        # 更新LLM结果
        llm_result = llm_res
        response["strategies"] = strategies
        response["example_comments"] = example_comments
        response["llm_analysis"] = llm_result  # 单独存储LLM分析结果
        
        logger.info(f"LLM analysis completed in {round(time.time() - llm_start, 2)}s")
    except Exception as e:
        logger.warning(f"Failed to get LLM strategies and examples: {e}")
        # 设置默认值
        response["strategies"] = "• Thank you for taking the time to watch and comment\n• Respond positively to constructive feedback\n• Stay professional even with negative comments\n• Use feedback to improve future content"
        response["example_comments"] = default_examples
    
    # 更新总处理时间
    response["duration_s"] = round(time.time() - start, 2)
    
    # 如果两种分析都没有结果，返回错误
    if not nlp_result and not llm_result:
        return {
            "success": False,
            "message": "Both NLP and LLM analysis failed",
            "example_comments": default_examples  # 确保返回一些示例
        }
    
    logger.info(f"Analysis completed in {response['duration_s']}s")
    return response 


class Analyzer:
    def __init__(self):
        self.youtube_client = YouTubeClient()
        self.bert_model = None
        self.openai_client = OpenAIClient()
        self.openrouter_client = OpenRouterClient()
        
        try:
            # Try to load the BERT model
            logger.info("Initializing BERT model...")
            self.bert_model = BERTModel()
            logger.info("BERT model initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing BERT model: {str(e)}")
            self.bert_model = None

    def analyse_video_comments(self, url: str, limit: int = 10) -> Dict[str, Any]:
        """
        Analyze YouTube video comments for sentiment and toxicity,
        then generate response strategies and example responses.
        
        Args:
            url: YouTube video URL
            limit: Maximum number of comments to analyze
            
        Returns:
            Dictionary with analysis results
        """
        start_time = time.time()
        
        # Initialize response container
        response = {
            "success": True,
            "method": "unknown",
            "duration": 0,
            "nlp_analysis": None,
            "llm_analysis": None,
            "strategies": None,
            "example_comments": None
        }
        
        try:
            # 1. Get comments from YouTube
            logger.info(f"Fetching comments for {url}")
            comments = self.youtube_client.get_video_comments(url, limit)
            
            if not comments:
                return {
                    "success": False,
                    "message": "No comments found or unable to retrieve comments"
                }
                
            logger.info(f"Retrieved {len(comments)} comments")
            
            # 2. Process comments with both NLP and LLM in parallel
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Submit NLP analysis task
                nlp_future = executor.submit(self.process_with_nlp_model, comments)
                
                # Submit LLM analysis task
                llm_future = executor.submit(self.process_with_llm, comments, url)
                
                # Get results (this will wait for both tasks to complete)
                nlp_result = nlp_future.result()
                llm_result = llm_future.result()
            
            # 3. Combine results
            response["nlp_analysis"] = nlp_result
            response["llm_analysis"] = llm_result
            response["strategies"] = llm_result.get("strategies") if llm_result and "strategies" in llm_result else None
            response["example_comments"] = llm_result.get("example_comments") if llm_result and "example_comments" in llm_result else None
            
            # Determine the primary method used
            if nlp_result:
                response["method"] = "local_model"
            elif llm_result:
                response["method"] = "openrouter"
            
            logger.info("Analysis completed successfully")
            
        except Exception as e:
            logger.error(f"Error during video comment analysis: {str(e)}")
            return {
                "success": False,
                "message": f"Analysis failed: {str(e)}"
            }
        finally:
            # Calculate duration
            duration = time.time() - start_time
            response["duration"] = round(duration, 2)
            
        return response
        
    def process_with_nlp_model(self, comments: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Process comments using the local BERT model for sentiment and toxicity analysis"""
        if not self.bert_model:
            logger.info("Local NLP model not available")
            return None
            
        try:
            logger.info("Starting local NLP model analysis")
            
            # Extract just the comment text
            comment_texts = [comment['text'] for comment in comments]
            
            # Perform sentiment analysis
            sentiment_results = self.bert_model.predict_sentiment(comment_texts)
            
            # Perform toxicity analysis
            toxicity_results = self.bert_model.predict_toxicity(comment_texts)
            
            # Count sentiments
            sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
            for sentiment in sentiment_results:
                sentiment_counts[sentiment] += 1
                
            # Count toxicity types
            total_toxic = 0
            toxicity_counts = {
                "toxic": 0,
                "severe_toxic": 0,
                "obscene": 0,
                "threat": 0,
                "insult": 0,
                "identity_hate": 0
            }
            
            for toxic_result in toxicity_results:
                is_toxic = False
                for toxic_type, value in toxic_result.items():
                    if value:
                        toxicity_counts[toxic_type] += 1
                        is_toxic = True
                if is_toxic:
                    total_toxic += 1
            
            result = {
                "sentiment": sentiment_counts,
                "toxicity": {
                    "counts": toxicity_counts,
                    "total_toxic_comments": total_toxic
                }
            }
            
            logger.info("Local NLP model analysis completed")
            return result
            
        except Exception as e:
            logger.error(f"Error during NLP model processing: {str(e)}")
            return None

    def process_with_llm(self, comments: List[Dict[str, Any]], url: str) -> Optional[Dict[str, Any]]:
        """Process comments using the LLM model (OpenRouter) for analysis, strategies and examples"""
        try:
            logger.info("Starting LLM analysis")
            
            # Use OpenRouter client
            llm_response = self.openrouter_client.analyze_comments(comments, url)
            
            if not llm_response:
                logger.warning("OpenRouter returned no response")
                return None
                
            # Extract sentiment information if available
            sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
            strategies = None
            example_comments = None
            
            # If the LLM response contains structured information
            if isinstance(llm_response, dict):
                # Extract sentiment if available
                if "sentiment" in llm_response:
                    sentiment_counts = llm_response["sentiment"]
                
                # Extract strategies
                if "strategies" in llm_response:
                    strategies = llm_response["strategies"]
                
                # Extract example comments
                if "example_comments" in llm_response:
                    example_comments = llm_response["example_comments"]
            
            result = {
                "sentiment": sentiment_counts,
                "strategies": strategies,
                "example_comments": example_comments
            }
            
            logger.info("LLM analysis completed")
            return result
            
        except Exception as e:
            logger.error(f"Error during LLM processing: {str(e)}")
            return None

    def analyze_single_comment(self, comment_text: str) -> str:
        """Use OpenRouter to generate a response to a single comment"""
        try:
            logger.info(f"Analyzing single comment: {comment_text[:50]}...")
            response = self.openrouter_client.single_comment_analysis(comment_text)
            return response
        except Exception as e:
            logger.error(f"Error analyzing single comment: {str(e)}")
            return f"Error analyzing comment: {str(e)}" 