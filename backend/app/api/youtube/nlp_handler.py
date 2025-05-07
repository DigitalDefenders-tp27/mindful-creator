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

def load_models():
    """Load the sentiment and toxicity models"""
    global sentiment_model, sentiment_tokenizer, toxicity_model, toxicity_tokenizer
    
    try:
        # Load sentiment model
        sentiment_tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
        sentiment_model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
        
        # Load toxicity model
        toxicity_tokenizer = AutoTokenizer.from_pretrained("unitary/toxic-bert")
        toxicity_model = AutoModelForSequenceClassification.from_pretrained("unitary/toxic-bert")
        
        logger.info("Successfully loaded NLP models")
        return True
    except Exception as e:
        logger.error(f"Error loading NLP models: {e}")
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
    
    # Try to load models if not already loaded
    if sentiment_model is None or toxicity_model is None:
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
        
        # Process each comment
        for comment in comments[:limit]:
            # Analyze sentiment
            sentiment_inputs = sentiment_tokenizer(comment, return_tensors="pt", truncation=True, padding=True)
            with torch.no_grad():
                sentiment_outputs = sentiment_model(**sentiment_inputs)
                sentiment_scores = torch.softmax(sentiment_outputs.logits, dim=1)
                
                # Get sentiment label
                sentiment_label = sentiment_scores.argmax().item()
                sentiment_score = sentiment_scores[0][sentiment_label].item()
                
                # Map to our categories
                if sentiment_label == 1:  # Positive
                    sentiment_counts["Positive"] += 1
                else:  # Negative
                    sentiment_counts["Negative"] += 1
            
            # Analyze toxicity
            toxicity_inputs = toxicity_tokenizer(comment, return_tensors="pt", truncation=True, padding=True)
            with torch.no_grad():
                toxicity_outputs = toxicity_model(**toxicity_inputs)
                toxicity_scores = torch.sigmoid(toxicity_outputs.logits)
                
                # Check each toxicity category
                toxicity_labels = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]
                for i, label in enumerate(toxicity_labels):
                    if toxicity_scores[0][i].item() > 0.5:  # Threshold for toxicity
                        toxicity_counts[label] += 1
        
        # Create response
        result = {
            "sentiment": sentiment_counts,
            "toxicity": toxicity_counts
        }
        
        logger.info(f"NLP analysis complete. Sentiment: {sentiment_counts}, Toxicity: {toxicity_counts}")
        return result
        
    except Exception as e:
        logger.error(f"Error in NLP analysis: {e}")
        return None 