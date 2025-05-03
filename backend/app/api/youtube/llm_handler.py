"""Handle YouTube comments analysis with LLM integration."""
import os
import sys
import logging
from typing import List, Dict, Any, Optional
import time

# Ensure project root is on PYTHONPATH
proj_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(proj_root, '.env'))

# Setup logging
LOGLEVEL = os.getenv('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)
logger = logging.getLogger(__name__)

# API Configuration
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv('OPENROUTER_API_KEY')
MODEL_NAME = os.getenv('OPENROUTER_MODEL', 'deepseek/deepseek-chat-v3-0324:free')

# Log API configuration
logger.info(f"OpenRouter API key configured: {bool(API_KEY)}")
logger.info(f"Using model: {MODEL_NAME}")

# Create a session for better performance
_session = requests.Session()
if API_KEY:
    _session.headers.update({
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://mindful-creator.vercel.app/",  # Required by OpenRouter
        "X-Title": "Mindful Creator"  # Optional for OpenRouter analytics
    })
    logger.info("OpenRouter session configured successfully")
else:
    logger.error("OpenRouter API key not found in environment variables")

def analyse_youtube_comments(comments: List[str]) -> Dict[str, Any]:
    """
    Analyse a list of YouTube comments using LLM.
    
    Args:
        comments: List of comment strings from YouTube
        
    Returns:
        Dictionary with analysis results including strategies and example responses
    """
    if not comments:
        return {
            "status": "error",
            "message": "No comments provided for analysis"
        }
    
    if not API_KEY:
        logger.warning("OpenRouter API key not configured, using fallback response")
        return {
            "status": "partial",
            "strategies": "No specific strategies could be generated. OpenRouter API key is missing.",
            "example_comments": []
        }
    
    logger.info(f"Analyzing {len(comments)} comments with OpenRouter")
    
    # 设置超时和重试参数
    max_retries = 2
    timeout_seconds = 300  # 增加到5分钟，允许模型加载和处理时间
    
    # 使用异常处理和降级模式确保即使LLM调用失败也能返回有用的结果
    try:
        # Identify most critical comments
        toxic_comments = []
        try:
            # 设置超时，如果超时就使用一个小样本
            for attempt in range(max_retries):
                try:
                    logger.info(f"Identifying critical comments (attempt {attempt+1}/{max_retries})")
                    toxic_comments = identify_critical_comments(comments)
                    break
                except Exception as e:
                    logger.error(f"Error identifying critical comments (attempt {attempt+1}): {e}")
                    if attempt == max_retries - 1:  # 最后一次尝试失败
                        # 降级：从原始评论中选择一些样本
                        logger.warning("Failed to identify critical comments, using sample of original comments")
                        toxic_comments = comments[:min(3, len(comments))]
        except Exception as e:
            logger.error(f"Failed to identify critical comments: {e}")
            toxic_comments = comments[:min(3, len(comments))]
        
        # 确保有评论可以分析
        if not toxic_comments and comments:
            toxic_comments = comments[:min(3, len(comments))]
        
        # Generate strategies with timeout and retry
        strategies = ""
        for attempt in range(max_retries):
            try:
                logger.info(f"Generating response strategies (attempt {attempt+1}/{max_retries})")
                strategies = generate_response_strategies(toxic_comments)
                if strategies and not "API key is missing" in strategies:
                    break
            except Exception as e:
                logger.error(f"Error generating strategies (attempt {attempt+1}): {e}")
                if attempt == max_retries - 1:  # 最后一次尝试失败
                    strategies = generate_fallback_strategies(toxic_comments)
        
        # Generate example responses with timeout and retry
        example_responses = []
        for attempt in range(max_retries):
            try:
                logger.info(f"Generating example responses (attempt {attempt+1}/{max_retries})")
                example_responses = generate_example_responses(toxic_comments)
                if example_responses:
                    break
            except Exception as e:
                logger.error(f"Error generating example responses (attempt {attempt+1}): {e}")
                if attempt == max_retries - 1:  # 最后一次尝试失败
                    example_responses = generate_fallback_examples(toxic_comments)
        
        # 确保总是返回有效的策略和示例
        if not strategies:
            strategies = generate_fallback_strategies(toxic_comments)
        
        if not example_responses:
            example_responses = generate_fallback_examples(toxic_comments)
        
        return {
            "status": "success",
            "strategies": strategies,
            "example_comments": example_responses
        }
    except Exception as e:
        logger.error(f"Error in LLM analysis: {e}")
        # 确保返回降级结果，而不是错误
        return {
            "status": "partial",
            "strategies": generate_fallback_strategies(comments[:min(3, len(comments))]),
            "example_comments": generate_fallback_examples(comments[:min(3, len(comments))])
        }

def identify_critical_comments(comments: List[str], max_comments: int = 3) -> List[str]:
    """
    Identify the most critical or negative comments that need addressing.
    
    Args:
        comments: List of comment strings
        max_comments: Maximum number of critical comments to return
        
    Returns:
        List of the most critical comments
    """
    if not API_KEY:
        logger.error("Cannot identify critical comments: API key missing")
        return []
    
    # Prepare prompt for the LLM
    comments_text = "\n".join([f"- {comment}" for comment in comments])
    prompt = f"""Analyse these YouTube comments and identify the {max_comments} most critical or negative ones that would require careful response:

{comments_text}

IMPORTANT: Return ONLY the exact text of the {max_comments} most critical comments, one per line.
DO NOT add any introductory text, summaries, or phrases like "The most critical comments are:".
DO NOT number the comments or add any formatting.
ONLY return the raw comment text, exactly as provided in the input.
"""
    
    system_message = """You are an expert content moderation assistant. Your task is to identify comments 
    that are negative, critical, or potentially harmful. Focus on comments that have personal attacks, 
    offensive language, or harsh criticism rather than constructive feedback.
    
    When presenting your findings, NEVER add introductory phrases like "The most critical or negative comments are:".
    ONLY present the exact comment text, one comment per line, with no additional text or formatting."""
    
    try:
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000
        }
        
        resp = _session.post(API_URL, json=payload, timeout=300)
        resp.raise_for_status()
        data = resp.json()
        
        # Log the API original response for debugging
        logger.debug(f"OpenRouter API original response: {data}")
        
        # Check response structure
        if 'choices' not in data:
            logger.error(f"API response missing 'choices' key: {data}")
            return comments[:min(max_comments, len(comments))]
            
        choices = data.get('choices', [])
        if not choices or len(choices) == 0:
            logger.error("API response choices list is empty")
            return comments[:min(max_comments, len(comments))]
            
        first_choice = choices[0]
        if not isinstance(first_choice, dict):
            logger.error(f"choices[0] is not a dictionary type: {type(first_choice)}")
            return comments[:min(max_comments, len(comments))]
            
        message = first_choice.get('message', {})
        if not isinstance(message, dict):
            logger.error(f"message is not a dictionary type: {type(message)}")
            return comments[:min(max_comments, len(comments))]
            
        content = message.get('content', '')
        if content:
            # Extract the list of critical comments
            critical_comments = [line.strip() for line in content.strip().split('\n') if line.strip()]
            
            # Additional filter to remove potential introductory lines like "The most critical comments are:"
            filtered_comments = []
            for comment in critical_comments:
                # Skip lines that appear to be introductory text rather than comments
                if any(phrase in comment.lower() for phrase in [
                    "the most critical", "here are", "these are", "critical comments", 
                    "negative comments", "comments are", "identified", "response", "would require"
                ]):
                    logger.warning(f"Filtered out possible introductory text: {comment}")
                    continue
                filtered_comments.append(comment)
            
            logger.info(f"Extracted {len(filtered_comments)} comments from LLM response")
            return filtered_comments[:max_comments]  # Ensure we don't exceed max_comments
            
        logger.warning("No content returned from LLM")
    except Exception as e:
        logger.error(f"Error identifying critical comments: {e}")
        import traceback
        logger.error(traceback.format_exc())
    
    # Fallback to a simple approach if LLM fails
    # Just return a subset of the original comments (first few)
    return comments[:min(max_comments, len(comments))]

def generate_response_strategies(critical_comments: List[str]) -> str:
    """
    Generate overall strategies for handling critical comments.
    
    Args:
        critical_comments: List of critical comments to address
        
    Returns:
        String with general strategies for handling these types of comments
    """
    if not API_KEY:
        logger.error("API_KEY is not set - cannot generate strategies")
        return "No specific strategies could be generated. API key is missing."
        
    if not critical_comments:
        logger.warning("No critical comments provided to generate strategies")
        return "No specific strategies could be generated. No critical comments found."
    
    comments_text = "\n".join([f"- {comment}" for comment in critical_comments])
    prompt = f"""Based on these critical YouTube comments:

{comments_text}

Provide 3-5 brief, professional strategies for content creators to respond effectively. Include:
1. General principles for handling criticism
2. Specific techniques based on comment themes
3. Tips for maintaining creator wellbeing

Format as very concise, actionable bullet points.
BE EXTREMELY CONCISE. USE NO MORE THAN 2-3 SHORT SENTENCES PER POINT.
"""
    
    system_message = """You are a digital wellbeing expert specialising in social media and online content creation. 
    You provide balanced, practical advice in the most concise format possible. 
    Your guidance must be extremely brief, specific, and focused on actionable steps.
    Avoid unnecessary elaboration, background information, or lengthy explanations."""
    
    # Try up to 2 times with a small delay
    max_attempts = 2
    for attempt in range(max_attempts):
        try:
            logger.info(f"Generating strategies - attempt {attempt+1}/{max_attempts}")
            
            payload = {
                "model": MODEL_NAME,
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 500,  # Reduced token limit to encourage brevity
                "temperature": 0.3  # Lower temperature for more focused, predictable responses
            }
            
            resp = _session.post(API_URL, json=payload, timeout=300)
            resp.raise_for_status()
            data = resp.json()
            
            # Log the API response for debugging
            logger.debug(f"OpenRouter API response for strategies: {data}")
            
            content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
            if content and len(content.strip()) > 0:
                return content.strip()
            
            logger.warning(f"No content returned from LLM for strategies on attempt {attempt+1}")
            
            # Wait a bit before retrying
            if attempt < max_attempts - 1:
                time.sleep(1)  # Sleep for 1 second before retrying
                
        except Exception as e:
            logger.error(f"Error generating strategies on attempt {attempt+1}: {e}")
            import traceback
            logger.error(traceback.format_exc())
            
            # Wait a bit before retrying
            if attempt < max_attempts - 1:
                time.sleep(1)  # Sleep for 1 second before retrying
    
    # 修改这里，不再使用预设内容，而是返回错误消息
    logger.warning("All attempts to generate strategies failed")
    return "Could not generate specific strategies at this time."

def generate_example_responses(critical_comments: List[str]) -> List[Dict[str, str]]:
    """
    Generate example responses for each critical comment.
    
    Args:
        critical_comments: List of critical comments to respond to
        
    Returns:
        List of dictionaries with original comments and suggested responses
    """
    if not API_KEY:
        logger.error("API_KEY is not set - cannot generate example responses")
        return []
        
    if not critical_comments:
        logger.warning("No critical comments provided to generate example responses")
        return []
    
    responses = []
    
    for comment in critical_comments:
        # Create a prompt specific to this comment
        prompt = f"""This is a critical comment on my YouTube video:

"{comment}"

Write a thoughtful, professional response that:
1. Acknowledges the comment without being defensive
2. Maintains a positive tone
3. Provides minimal clarification if needed
4. Ends with a forward-looking statement

KEEP IT EXTREMELY BRIEF. Maximum 50 words total. Be direct and to the point.
"""
        
        system_message = """You are a professional community manager who specialises in crafting 
        extremely concise responses to difficult social media comments. Your responses are authentic and clear,
        but prioritize brevity above all else. Keep responses under 50 words."""
        
        response_text = None
        # Try up to 2 times with a small delay
        max_attempts = 2
        
        for attempt in range(max_attempts):
            try:
                logger.info(f"Generating response for comment (attempt {attempt+1}/{max_attempts}): {comment[:50]}...")
                
                payload = {
                    "model": MODEL_NAME,
                    "messages": [
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 250,  # Reduced from 500
                    "temperature": 0.4  # Slightly lower temperature for more focused responses
                }
                
                resp = _session.post(API_URL, json=payload, timeout=300)
                resp.raise_for_status()
                data = resp.json()
                
                # Get the model's response
                content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
                if content and len(content.strip()) > 0:
                    response_text = content.strip()
                    break  # Successfully got a response, break the retry loop
                
                logger.warning(f"No content returned for comment on attempt {attempt+1}: {comment[:50]}...")
                
                # Wait a bit before retrying
                if attempt < max_attempts - 1:
                    time.sleep(1)
                    
            except Exception as e:
                logger.error(f"Error generating response on attempt {attempt+1}: {e}")
                
                # Wait a bit before retrying
                if attempt < max_attempts - 1:
                    time.sleep(1)
        
        # 修改这里，不再使用预设内容，而是跳过该评论
        if not response_text:
            logger.warning(f"Could not generate response for comment: {comment[:50]}... - skipping")
            continue
        
        # Add to our responses list
        responses.append({
            "comment": comment,
            "response": response_text
        })
    
    return responses

# 添加降级函数
def generate_fallback_strategies(comments: List[str]) -> str:
    """生成预定义的应对策略"""
    return """• Keep your cool when responding to negative comments - no need to get defensive or worked up
• Focus on the fair dinkum feedback while ignoring the personal attacks
• Show appreciation for constructive criticism even when it's delivered a bit harshly
• Set clear boundaries by moderating truly toxic or harmful comments
• Remember you don't have to respond to every negative comment - sometimes it's best to let it go"""

def generate_fallback_examples(comments: List[str]) -> List[Dict[str, str]]:
    """生成预定义的示例回复"""
    # 确保即使没有评论也能返回有用的示例
    if not comments:
        return [
            {
                "comment": "Your video was absolute rubbish, you clearly don't know what you're on about!",
                "response": "Thanks for watching, mate. I'm always keen to improve my content - if you've got specific feedback, I'd love to hear it."
            },
            {
                "comment": "This makes no sense. You're just waffling on about nothing important.",
                "response": "Cheers for taking the time to watch. I'm working on making my explanations clearer - if a specific part confused you, let me know!"
            }
        ]
    
    # 为实际评论生成通用但合理的回复
    results = []
    for i, comment in enumerate(comments[:3]):  # 最多处理3条评论
        # 截取评论前100个字符作为预览
        preview = comment[:100] + "..." if len(comment) > 100 else comment
        
        # 基于评论长度选择不同的标准回复
        if len(comment) < 30:
            response = "Thanks for your feedback, mate. Really appreciate you taking the time to share your thoughts!"
        elif "?" in comment:
            response = "Thanks for your question! I'll have a proper crack at this topic in my next video."
        else:
            response = "I value your perspective. Cheers for engaging with my content - feedback like this helps me improve!"
        
        results.append({
            "comment": preview,
            "response": response
        })
    
    return results
