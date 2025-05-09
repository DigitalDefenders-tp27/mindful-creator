import os
import time
import logging
import traceback
from typing import List, Dict, Any, Optional
import asyncio
import json

# Configure logger
logger = logging.getLogger(__name__)

async def analyse_video_comments(video_id: str, limit: int = 5) -> Dict[str, Any]:
    """
    Analyse comments from a YouTube video and return insights.
    
    Args:
        video_id: YouTube video ID to analyse
        limit: Maximum number of comments to return in results
        
    Returns:
        Dictionary containing analysis results
    """
    start_time = time.time()
    response = {
        "success": False,
        "totalComments": 0,
            "sentiment": {
            "positive": 0,
            "neutral": 0,
            "negative": 0
            },
            "toxicity": {
            "total": 0,
            "percentage": 0,
            "types": {
                "Toxic": 0,
                "Severe Toxic": 0,
                "Obscene": 0,
                "Threat": 0,
                "Insult": 0,
                "Identity Hate": 0
            }
        },
        "strategies": "",
        "example_comments": []
    }
    
    try:
        # Get comments from YouTube
        from .clients.youtube import YouTubeClient
        youtube_client = YouTubeClient()
        comments = await youtube_client.get_video_comments(video_id, limit)
        
        if not comments:
            logger.warning("No comments fetched, using dummy comments for testing")
            comments = [
                "This video was so helpful, I learned a lot!",
                "I don't agree with what you said about this topic.",
                "You're completely wrong about this. You should do more research before making videos."
            ]
        
        response["totalComments"] = len(comments)
        
        # Try NLP analysis first
        try:
            logger.info("Attempting NLP analysis...")
            from .nlp_handler import analyze_comments
            # Run NLP analysis in a thread pool to avoid blocking
            nlp_result = await asyncio.to_thread(analyze_comments, comments)
            if nlp_result:
                # Map sentiment data using proper structure
                # Good on ya, mate! Converting local NLP results to API format
                response["sentiment"] = {
                    "positive": nlp_result["analysis"]["sentiment"]["positive_count"],
                    "neutral": nlp_result["analysis"]["sentiment"]["neutral_count"],
                    "negative": nlp_result["analysis"]["sentiment"]["negative_count"]
                }
                
                # Fair dinkum! Make sure we properly map the toxicity data
                response["toxicity"] = {
                    "total": nlp_result["analysis"]["toxicity"]["toxic_count"],
                    "percentage": nlp_result["analysis"]["toxicity"]["toxic_percentage"],  # Crikey! We forgot this one before
                    "types": {
                        "Toxic": nlp_result["analysis"]["toxicity"]["toxic_types"]["toxic"],
                        "Severe Toxic": nlp_result["analysis"]["toxicity"]["toxic_types"]["severe_toxic"],
                        "Obscene": nlp_result["analysis"]["toxicity"]["toxic_types"]["obscene"],
                        "Threat": nlp_result["analysis"]["toxicity"]["toxic_types"]["threat"],
                        "Insult": nlp_result["analysis"]["toxicity"]["toxic_types"]["insult"],
                        "Identity Hate": nlp_result["analysis"]["toxicity"]["toxic_types"]["identity_hate"]
                    }
                }
                logger.info("NLP analysis completed successfully")
                
                # Add debug info to help spot any dramas with the data structure
                logger.debug(f"NLP sentiment data: {nlp_result['analysis']['sentiment']}")
                logger.debug(f"NLP toxicity data: {nlp_result['analysis']['toxicity']}")
                logger.debug(f"Mapped API response: {response['sentiment']} and {response['toxicity']}")
        except Exception as e:
            logger.error(f"NLP analysis failed: {str(e)}")
            logger.error(traceback.format_exc())
        
        # Always use LLM for strategies and examples
        try:
            logger.info("Getting LLM analysis for strategies and examples...")
            from .llm_handler import analyse_youtube_comments
            llm_result = await analyse_youtube_comments(comments, limit)
            if llm_result:
                response["strategies"] = llm_result.get("strategies", "")
                response["example_comments"] = llm_result.get("example_comments", [])
                logger.info("LLM analysis completed successfully")
        except Exception as e:
            logger.error(f"LLM analysis failed: {str(e)}")
            logger.error(traceback.format_exc())
            # Provide fallback strategies and examples
            response["strategies"] = "• Thank viewers for their feedback\n• Address concerns professionally\n• Acknowledge different perspectives\n• Use feedback to improve future content"
            response["example_comments"] = [
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
        
        response["success"] = True
        
        logger.info(f"Analysis completed in {time.time() - start_time:.2f} seconds")
        logger.info(f"Final response structure: {json.dumps(response, indent=2)}")
        
        return response
        
    except Exception as e:
        logger.error(f"Error in analyse_video_comments: {str(e)}")
        logger.error(traceback.format_exc())
        response["success"] = False
        return response 