import os
import logging
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import List, Dict, Any

# Configure logger
logger = logging.getLogger(__name__)

# Initialize models and tokenizers
sentiment_model = None
sentiment_tokenizer = None
toxicity_model = None
toxicity_tokenizer = None

# Define thresholds
SENTIMENT_THRESHOLD = 0.6
TOXICITY_THRESHOLD = 0.5
SEVERE_TOXICITY_THRESHOLD = 0.7

def load_models():
    """Load the sentiment and toxicity models"""
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
        
        logger.info("Successfully loaded all NLP models")
        return True
    except Exception as e:
        logger.error(f"Error loading NLP models: {str(e)}")
        return False

def analyze_comments(comments: List[str], limit: int = 5) -> Dict[str, Any]:
    """
    Analyze comments using local NLP models for sentiment and toxicity.
    
    Args:
        comments: List of comment strings
        limit: Maximum number of comments to analyze
        
    Returns:
        Dictionary containing sentiment and toxicity analysis
    """
    global sentiment_model, sentiment_tokenizer, toxicity_model, toxicity_tokenizer
    
    if not comments:
        logger.warning("No comments provided for analysis")
        return {
            "sentiment": {"Positive": 0, "Neutral": 0, "Negative": 0},
            "toxicity": {
                "toxic": 0, "severe_toxic": 0, "obscene": 0,
                "threat": 0, "insult": 0, "identity_hate": 0
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
        sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
        toxicity_counts = {
            "toxic": 0,
            "severe_toxic": 0,
            "obscene": 0,
            "threat": 0,
            "insult": 0,
            "identity_hate": 0
        }
        
        logger.info(f"Starting analysis of {min(len(comments), limit)} comments")
        
        # Process each comment
        for i, comment in enumerate(comments[:limit]):
            if not comment or not isinstance(comment, str):
                logger.warning(f"Skipping invalid comment at index {i}")
                continue
                
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
                    
                    # Determine sentiment category with neutral threshold
                    if positive_score > SENTIMENT_THRESHOLD:
                        sentiment_counts["Positive"] += 1
                    elif negative_score > SENTIMENT_THRESHOLD:
                        sentiment_counts["Negative"] += 1
                    else:
                        sentiment_counts["Neutral"] += 1
                
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
                            toxicity_counts[label] += 1
                            if label == "toxic" and score > SEVERE_TOXICITY_THRESHOLD:
                                toxicity_counts["severe_toxic"] += 1
                            logger.debug(f"Found {label} in comment {i+1} with score {score:.2f}")
            
            except Exception as e:
                logger.error(f"Error processing comment {i+1}: {str(e)}")
                continue
        
        # Calculate total toxic comments
        total_toxic = sum(toxicity_counts.values())
        
        # Create response with additional metadata
        result = {
            "sentiment": sentiment_counts,
            "toxicity": {
                "counts": toxicity_counts,
                "total_toxic": total_toxic,
                "total_comments": len(comments[:limit]),
                "toxic_percentage": (total_toxic / len(comments[:limit]) * 100) if comments else 0
            }
        }
        
        logger.info(f"NLP analysis complete. Results: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error in NLP analysis: {str(e)}", exc_info=True)
        return None 