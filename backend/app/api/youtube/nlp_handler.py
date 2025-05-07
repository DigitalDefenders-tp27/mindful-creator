import os
import logging
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import List, Dict, Any, Optional

# Configure logger
logger = logging.getLogger(__name__)

# Initialize models and tokenizers
sentiment_model: Optional[AutoModelForSequenceClassification] = None
sentiment_tokenizer: Optional[AutoTokenizer] = None
toxicity_model: Optional[AutoModelForSequenceClassification] = None
toxicity_tokenizer: Optional[AutoTokenizer] = None

# Define thresholds
SENTIMENT_THRESHOLD = 0.6
TOXICITY_THRESHOLD = 0.5
SEVERE_TOXICITY_THRESHOLD = 0.7

def load_models() -> bool:
    """
    Load the sentiment and toxicity models.
    
    Returns:
        bool: True if models loaded successfully, False otherwise
    """
    global sentiment_model, sentiment_tokenizer, toxicity_model, toxicity_tokenizer
    
    try:
        logger.info("Starting to load NLP models...")
        
        # Load sentiment model
        logger.info("Loading sentiment model...")
        sentiment_tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
        sentiment_model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
        
        # Load toxicity model
        logger.info("Loading toxicity model...")
        toxicity_tokenizer = AutoTokenizer.from_pretrained("unitary/toxic-bert")
        toxicity_model = AutoModelForSequenceClassification.from_pretrained("unitary/toxic-bert")
        
        # Set models to evaluation mode
        sentiment_model.eval()
        toxicity_model.eval()
        
        # Verify models are loaded correctly
        if sentiment_model is None or toxicity_model is None:
            raise RuntimeError("Models failed to load properly")
            
        logger.info("Successfully loaded all NLP models")
        return True
    except Exception as e:
        logger.error(f"Error loading NLP models: {str(e)}", exc_info=True)
        return False

def analyze_comments(comments: List[str], limit: int = 100) -> Optional[Dict]:
    """
    Analyze comments for sentiment and toxicity.
    
    Args:
        comments: List of comments to analyze
        limit: Maximum number of comments to analyze
        
    Returns:
        Dict containing analysis results or None if analysis fails
    """
    if not comments:
        logger.warning("No comments provided for analysis")
        return None
        
    if not isinstance(comments, list):
        logger.error(f"Invalid comments type: {type(comments)}")
        return None
        
    if not isinstance(limit, int) or limit <= 0:
        logger.warning(f"Invalid limit value: {limit}, using default of 100")
        limit = 100
    
    # Initialize models if not already loaded
    if not load_models():
        logger.error("Failed to load models")
        return None
    
    try:
        # Filter and clean comments
        valid_comments = []
        for comment in comments:
            if isinstance(comment, str) and comment.strip():
                valid_comments.append(comment.strip())
            else:
                logger.warning(f"Skipping invalid comment: {comment}")
        
        if not valid_comments:
            logger.warning("No valid comments to analyze")
            return None
            
        # Limit number of comments
        comments_to_analyze = valid_comments[:limit]
        logger.info(f"Analyzing {len(comments_to_analyze)} comments")
        
        # Initialize counters
        sentiment_counts = {
            "positive": 0,
            "neutral": 0,
            "negative": 0
        }
        
        toxicity_counts = {
            "Toxic": 0,
            "Severe Toxic": 0,
            "Obscene": 0,
            "Threat": 0,
            "Insult": 0,
            "Identity Hate": 0
        }
        
        total_toxic = 0
        
        # Process each comment
        for comment in comments_to_analyze:
            try:
                # Sentiment analysis
                sentiment_scores = sentiment_model(comment)[0]
                sentiment_label = sentiment_scores['label']
                sentiment_score = sentiment_scores['score']
                
                logger.debug(f"Comment sentiment: {sentiment_label} (score: {sentiment_score:.3f})")
                
                if sentiment_score >= SENTIMENT_THRESHOLD:
                    sentiment_counts[sentiment_label.lower()] += 1
                
                # Toxicity analysis
                toxicity_scores = toxicity_model(comment)[0]
                
                # Log toxicity scores for debugging
                logger.debug(f"Toxicity scores for comment: {toxicity_scores}")
                
                # Check each toxicity category
                for category, score in toxicity_scores.items():
                    if score >= TOXICITY_THRESHOLD:
                        toxicity_counts[category] += 1
                        if category == "Toxic":
                            total_toxic += 1
                
            except Exception as e:
                logger.error(f"Error processing comment: {str(e)}")
                continue
        
        # Calculate percentages
        total_comments = len(comments_to_analyze)
        toxic_percentage = (total_toxic / total_comments * 100) if total_comments > 0 else 0
        
        # Create response
        result = {
            "sentiment": {
                "positive": sentiment_counts["positive"],
                "neutral": sentiment_counts["neutral"],
                "negative": sentiment_counts["negative"]
            },
            "toxicity": {
                "total": total_toxic,
                "types": toxicity_counts,
                "percentage": toxic_percentage
            },
            "total_comments": total_comments
        }
        
        logger.info(f"NLP analysis completed. Found {total_toxic} toxic comments ({toxic_percentage:.1f}%)")
        logger.debug(f"Final result format: {result}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error in analyze_comments: {str(e)}")
        return None 