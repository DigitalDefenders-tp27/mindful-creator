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

def analyze_comments(comments: List[str], limit: int = 5) -> Optional[Dict[str, Any]]:
    """
    Analyze comments using local NLP models for sentiment and toxicity.
    
    Args:
        comments: List of comment strings
        limit: Maximum number of comments to analyze
        
    Returns:
        Dictionary containing sentiment and toxicity analysis, or None if analysis fails
    """
    global sentiment_model, sentiment_tokenizer, toxicity_model, toxicity_tokenizer
    
    # Input validation
    if not isinstance(comments, list):
        logger.error("Comments must be a list")
        return None
        
    if not isinstance(limit, int) or limit < 1:
        logger.error("Limit must be a positive integer")
        return None
    
    if not comments:
        logger.warning("No comments provided for analysis")
        return {
            "sentiment": {
                "positive_count": 0,
                "neutral_count": 0,
                "negative_count": 0
            },
            "toxicity": {
                "toxic_count": 0,
                "severe_toxic_count": 0,
                "obscene_count": 0,
                "threat_count": 0,
                "insult_count": 0,
                "identity_hate_count": 0,
                "toxic_percentage": 0.0,
                "toxic_types": {
                    "toxic": 0,
                    "severe_toxic": 0,
                    "obscene": 0,
                    "threat": 0,
                    "insult": 0,
                    "identity_hate": 0
                }
            }
        }
    
    # Try to load models if not already loaded
    if sentiment_model is None or toxicity_model is None:
        logger.info("Models not loaded, attempting to load now...")
        if not load_models():
            logger.error("Failed to load NLP models")
            return None
    
    try:
        # Initialize counters
        sentiment_counts = {
            "positive_count": 0,
            "neutral_count": 0,
            "negative_count": 0
        }
        toxicity_counts = {
            "toxic_count": 0,
            "severe_toxic_count": 0,
            "obscene_count": 0,
            "threat_count": 0,
            "insult_count": 0,
            "identity_hate_count": 0
        }
        toxic_types = {
            "toxic": 0,
            "severe_toxic": 0,
            "obscene": 0,
            "threat": 0,
            "insult": 0,
            "identity_hate": 0
        }
        
        # Filter and clean comments
        valid_comments = [
            comment.strip() 
            for comment in comments[:limit] 
            if isinstance(comment, str) and comment.strip()
        ]
        
        logger.info(f"Starting analysis of {len(valid_comments)} valid comments")
        
        # Process each comment
        for i, comment in enumerate(valid_comments):
            logger.debug(f"Processing comment {i+1}: {comment[:50]}...")
            
            try:
                # Analyze sentiment
                sentiment_inputs = sentiment_tokenizer(comment, return_tensors="pt", truncation=True, padding=True)
                with torch.no_grad():
                    sentiment_outputs = sentiment_model(**sentiment_inputs)
                    sentiment_scores = torch.softmax(sentiment_outputs.logits, dim=1)
                    
                    # Get sentiment scores
                    positive_score = sentiment_scores[0][1].item()
                    negative_score = sentiment_scores[0][0].item()
                    
                    logger.debug(f"Comment {i+1} sentiment scores - Positive: {positive_score:.2f}, Negative: {negative_score:.2f}")
                    
                    # Determine sentiment category with neutral threshold
                    if positive_score > SENTIMENT_THRESHOLD:
                        sentiment_counts["positive_count"] += 1
                    elif negative_score > SENTIMENT_THRESHOLD:
                        sentiment_counts["negative_count"] += 1
                    else:
                        sentiment_counts["neutral_count"] += 1
                
                # Analyze toxicity
                toxicity_inputs = toxicity_tokenizer(comment, return_tensors="pt", truncation=True, padding=True)
                with torch.no_grad():
                    toxicity_outputs = toxicity_model(**toxicity_inputs)
                    toxicity_scores = torch.sigmoid(toxicity_outputs.logits)
                    
                    # Check each toxicity category
                    toxicity_labels = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]
                    for j, label in enumerate(toxicity_labels):
                        score = toxicity_scores[0][j].item()
                        if score > TOXICITY_THRESHOLD:
                            toxicity_counts[f"{label}_count"] += 1
                            toxic_types[label] += 1
                            if label == "toxic" and score > SEVERE_TOXICITY_THRESHOLD:
                                toxicity_counts["severe_toxic_count"] += 1
                                toxic_types["severe_toxic"] += 1
                            logger.debug(f"Found {label} in comment {i+1} with score {score:.2f}")
            
            except Exception as e:
                logger.error(f"Error processing comment {i+1}: {str(e)}", exc_info=True)
                continue
        
        # Calculate total toxic comments and percentage
        # Exclude severe_toxic from total as it's a subset of toxic
        total_toxic = sum(
            count for key, count in toxicity_counts.items() 
            if key != "severe_toxic_count" and key != "toxic_percentage"
        )
        total_comments = len(valid_comments)
        toxic_percentage = (total_toxic / total_comments * 100) if total_comments > 0 else 0.0
        
        # Add toxic percentage to toxicity counts
        toxicity_counts["toxic_percentage"] = toxic_percentage
        toxicity_counts["toxic_types"] = toxic_types
        
        # Create response with the expected format
        result = {
            "sentiment": sentiment_counts,
            "toxicity": toxicity_counts
        }
        
        logger.info(f"NLP analysis complete. Results: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error in NLP analysis: {str(e)}", exc_info=True)
        return None 