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
    logger.info("=== Starting comment analysis ===")
    logger.info(f"Received {len(comments) if comments else 0} comments with limit {limit}")
    
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
    logger.info("Checking if models are loaded...")
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
        
        logger.info(f"Found {len(valid_comments)} valid comments out of {len(comments)} total")
        
        if not valid_comments:
            logger.warning("No valid comments to analyze")
            return None
            
        # Limit number of comments
        comments_to_analyze = valid_comments[:limit]
        logger.info(f"Analyzing {len(comments_to_analyze)} comments (limited from {len(valid_comments)})")
        
        # Initialize counters
        sentiment_counts = {
            "positive": 0,
            "neutral": 0,
            "negative": 0
        }
        
        toxicity_counts = {
            "toxic": 0,
            "severe_toxic": 0,
            "obscene": 0,
            "threat": 0,
            "insult": 0,
            "identity_hate": 0
        }
        
        total_toxic = 0
        
        # Process each comment
        logger.info("Starting sentiment and toxicity analysis...")
        for i, comment in enumerate(comments_to_analyze, 1):
            try:
                logger.debug(f"Processing comment {i}/{len(comments_to_analyze)}")
                
                # Tokenize comment for sentiment analysis
                sentiment_inputs = sentiment_tokenizer(comment, return_tensors="pt", truncation=True, padding=True)
                with torch.no_grad():
                    sentiment_outputs = sentiment_model(**sentiment_inputs)
                    sentiment_scores = torch.softmax(sentiment_outputs.logits, dim=1)[0]
                
                # Get sentiment label and score
                sentiment_label = "positive" if sentiment_scores[1] > sentiment_scores[0] else "negative"
                sentiment_score = float(sentiment_scores[1] if sentiment_label == "positive" else sentiment_scores[0])
                
                logger.debug(f"Comment {i} sentiment: {sentiment_label} (score: {sentiment_score:.3f})")
                
                # Update sentiment counts with more precise thresholds
                if sentiment_score >= 0.8:  # Strong positive
                    sentiment_counts["positive"] += 1
                elif sentiment_score <= 0.2:  # Strong negative
                    sentiment_counts["negative"] += 1
                else:  # Neutral
                    sentiment_counts["neutral"] += 1
                
                # Tokenize comment for toxicity analysis
                toxicity_inputs = toxicity_tokenizer(comment, return_tensors="pt", truncation=True, padding=True)
                with torch.no_grad():
                    toxicity_outputs = toxicity_model(**toxicity_inputs)
                    toxicity_scores = torch.sigmoid(toxicity_outputs.logits)[0]
                
                # Check each toxicity category with more precise thresholds
                is_toxic = False
                for idx, category in enumerate(toxicity_counts.keys()):
                    score = float(toxicity_scores[idx])
                    if score >= 0.7:  # Higher threshold for toxicity
                        toxicity_counts[category] += 1
                        is_toxic = True
                        logger.debug(f"Incremented {category} count to {toxicity_counts[category]} (score: {score:.3f})")
                
                if is_toxic:
                    total_toxic += 1
                    logger.debug(f"Incremented total toxic count to {total_toxic}")
                
            except Exception as e:
                logger.error(f"Error processing comment {i}: {str(e)}", exc_info=True)
                continue
        
        # Calculate percentages
        total_comments = len(comments_to_analyze)
        toxic_percentage = (total_toxic / total_comments * 100) if total_comments > 0 else 0
        
        logger.info(f"Analysis complete. Results:")
        logger.info(f"- Total comments analyzed: {total_comments}")
        logger.info(f"- Sentiment breakdown: {sentiment_counts}")
        logger.info(f"- Toxicity breakdown: {toxicity_counts}")
        logger.info(f"- Total toxic comments: {total_toxic} ({toxic_percentage:.1f}%)")
        
        # Create response matching frontend expectations
        result = {
            "total_comments": total_comments,
            "analysis": {
                "sentiment": {
                    "positive_count": sentiment_counts["positive"],
                    "neutral_count": sentiment_counts["neutral"],
                    "negative_count": sentiment_counts["negative"]
                },
                "toxicity": {
                    "toxic_count": total_toxic,
                    "toxic_percentage": toxic_percentage,
                    "toxic_types": toxicity_counts
                }
            },
            "strategies": "",  # This will be populated by the LLM service
            "example_comments": []  # This will be populated by the LLM service
        }
        
        logger.info("=== Analysis completed successfully ===")
        logger.debug(f"Final result format: {result}")
        
        return result
        
    except Exception as e:
        logger.error("=== Analysis failed with error ===", exc_info=True)
        logger.error(f"Error in analyze_comments: {str(e)}")
        return None 