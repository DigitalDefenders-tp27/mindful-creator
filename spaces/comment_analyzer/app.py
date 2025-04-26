import os
import gradio as gr
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from typing import List, Dict, Any

# 加载情感分析模型
sentiment_model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
sentiment_tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)
sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentiment_model_name)
sentiment_classifier = pipeline("sentiment-analysis", model=sentiment_model, tokenizer=sentiment_tokenizer)

# 加载毒性检测模型
toxicity_model_name = "unitary/toxic-bert"
toxicity_tokenizer = AutoTokenizer.from_pretrained(toxicity_model_name)
toxicity_model = AutoModelForSequenceClassification.from_pretrained(toxicity_model_name)
toxicity_classifier = pipeline("text-classification", model=toxicity_model, tokenizer=toxicity_tokenizer)

# 映射情感标签
sentiment_mapping = {
    "positive": "Positive",
    "neutral": "Neutral", 
    "negative": "Negative"
}

# 毒性标签
toxicity_categories = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]

# 毒性阈值（30%）
TOXICITY_THRESHOLD = 0.3

def analyze_comment(comment: str) -> Dict[str, Any]:
    """
    分析单个评论的情感和毒性
    
    Args:
        comment: 评论文本
        
    Returns:
        包含情感和毒性分析结果的字典
    """
    # 情感分析
    sentiment_result = sentiment_classifier(comment)[0]
    sentiment_label = sentiment_mapping.get(sentiment_result["label"], "Neutral")
    
    # 毒性分析
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
    批量分析评论列表并返回汇总结果
    
    Args:
        comments: 评论列表
        
    Returns:
        包含分析汇总结果的字典
    """
    if not comments:
        return {
            "error": "没有评论可供分析"
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
    
    # 分析每条评论
    for comment in comments:
        result = analyze_comment(comment)
        results.append(result)
        
        # 统计情感
        sentiment = result["sentiment"]
        sentiment_counts[sentiment] += 1
        
        # 统计毒性
        if result["is_toxic"]:
            toxic_comments.append(result)
            toxic_label = result["toxicity_label"]
            if toxic_label in toxic_types:
                toxic_types[toxic_label] += 1
    
    # 汇总结果
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
    处理评论列表并返回分析结果
    
    Args:
        comments_list: 评论列表
        
    Returns:
        分析结果摘要
    """
    return analyze_comments(comments_list)

# 创建Gradio接口
interface = gr.Interface(
    fn=process_comments,
    inputs=gr.List(gr.components.Textbox()),
    outputs=gr.components.JSON(),
    title="YouTube评论分析",
    description="分析YouTube评论的情感和毒性",
    examples=[
        [
            ["这个视频太棒了！我喜欢这个内容", 
             "这是我见过的最糟糕的视频", 
             "还行吧，一般般"]
        ]
    ]
)

# 启动应用
if __name__ == "__main__":
    interface.launch() 