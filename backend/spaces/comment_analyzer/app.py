import os
import gradio as gr
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from typing import List, Dict, Any

# Load sentiment analysis model
sentiment_model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
sentiment_tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)
sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentiment_model_name)
sentiment_classifier = pipeline("sentiment-analysis", model=sentiment_model, tokenizer=sentiment_tokenizer)

# Load toxicity detection model
toxicity_model_name = "unitary/toxic-bert"
toxicity_tokenizer = AutoTokenizer.from_pretrained(toxicity_model_name)
toxicity_model = AutoModelForSequenceClassification.from_pretrained(toxicity_model_name)
toxicity_classifier = pipeline("text-classification", model=toxicity_model, tokenizer=toxicity_tokenizer)

# Map sentiment labels
sentiment_mapping = {
    "positive": "Positive",
    "neutral": "Neutral", 
    "negative": "Negative"
}

# Toxicity categories
toxicity_categories = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]

# Toxicity threshold (30%)
TOXICITY_THRESHOLD = 0.3

def analyze_comment(comment: str) -> Dict[str, Any]:
    """
    Analyse a single comment for sentiment and toxicity
    
    Args:
        comment: Comment text
        
    Returns:
        Dictionary containing sentiment and toxicity analysis results
    """
    # Sentiment analysis
    sentiment_result = sentiment_classifier(comment)[0]
    sentiment_label = sentiment_mapping.get(sentiment_result["label"], "Neutral")
    
    # Toxicity analysis
    toxicity_result = toxicity_classifier(comment)[0]
    is_toxic = toxicity_result["score"] >= TOXICITY_THRESHOLD
    
    return {
        "text": comment,
        "sentiment": sentiment_label,
        "is_toxic": is_toxic,
        "toxicity_score": float(toxicity_result["score"]),
        "toxicity_label": toxicity_result["label"]
    }

def analyze_comments(comments: List[str]) -> Dict[str, Any]:
    """
    Batch analyse a list of comments and return aggregated results
    
    Args:
        comments: List of comments
        
    Returns:
        Dictionary containing aggregated analysis results
    """
    if not comments:
        return {
            "error": "No comments available for analysis"
        }
    
    results = []
    sentiment_counts = {
        "Positive": 0,
        "Neutral": 0,
        "Negative": 0
    }
    
    toxic_comments = []
    toxic_types = {
        "toxic": 0,
        "severe_toxic": 0,
        "obscene": 0,
        "threat": 0,
        "insult": 0,
        "identity_hate": 0
    }
    
    # Analyse each comment
    for comment in comments:
        result = analyze_comment(comment)
        results.append(result)
        
        # Count sentiments
        sentiment = result["sentiment"]
        sentiment_counts[sentiment] += 1
        
        # Count toxicities
        if result["is_toxic"]:
            toxic_comments.append(result)
            toxic_label = result["toxicity_label"]
            if toxic_label in toxic_types:
                toxic_types[toxic_label] += 1
    
    # Summarise results
    summary = {
        "total_comments": len(comments),
        "sentiment": {
            "positive_count": sentiment_counts["Positive"],
            "neutral_count": sentiment_counts["Neutral"],
            "negative_count": sentiment_counts["Negative"]
        },
        "toxicity": {
            "toxic_count": len(toxic_comments),
            "toxic_percentage": (len(toxic_comments) / len(comments)) * 100 if comments else 0,
            "toxic_types": toxic_types
        }
    }
    
    return summary

def process_comments(comments_list):
    """
    Process list of comments and return analysis results
    
    Args:
        comments_list: List of comments
        
    Returns:
        Analysis results summary
    """
    return analyze_comments(comments_list)

# Create Gradio interface
interface = gr.Interface(
    fn=process_comments,
    inputs=gr.List(gr.components.Textbox()),
    outputs=gr.components.JSON(),
    title="YouTube Comment Analyser",
    description="Analyse YouTube comments for sentiment and toxicity",
    examples=[
        [
            ["This video is amazing! I love the content", 
             "This is the worst video I've ever seen", 
             "It's okay, just average"]
        ]
    ]
)

# Launch the application
if __name__ == "__main__":
    interface.launch() 