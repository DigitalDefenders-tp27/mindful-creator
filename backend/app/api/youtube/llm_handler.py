"""Handle YouTube comments analysis with LLM integration."""
import os
import sys
import logging
from typing import List, Dict, Any, Optional
import time
import json
import re

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
MODEL_NAME = os.getenv('OPENROUTER_MODEL', 'deepseek/deepseek-prover-v2:free')

# Log API configuration
logger.info(f"OpenRouter API key configured: {bool(API_KEY)}")
logger.info(f"Using model: {MODEL_NAME}")

# Create a session for better performance
_session = requests.Session()
if API_KEY:
    _session.headers.update({
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        # "HTTP-Referer": "https://mindful-creator.vercel.app/",  # Required by OpenRouter
        # "X-Title": "Mindful Creator"  # Optional for OpenRouter analytics
    })
    logger.info("OpenRouter session configured successfully")
else:
    logger.error("OpenRouter API key not found in environment variables")

async def analyse_youtube_comments(comments: List[str], limit: int = 100) -> Dict[str, Any]:
    """
    Analyze YouTube comments and generate response strategies and examples.
    
    Args:
        comments: List of YouTube comment strings
        limit: Maximum number of comments to analyze
        
    Returns:
        Dictionary with sentiment analysis, strategies, and example responses
    """
    if not comments:
        logger.warning("No comments provided for analysis")
        return {
            "sentiment": {"Positive": 0, "Neutral": 0, "Negative": 0},
            "toxicity": {"toxic": 0, "severe_toxic": 0, "obscene": 0, "threat": 0, "insult": 0, "identity_hate": 0},
            "strategies": generate_fallback_strategies([]),
            "example_comments": generate_fallback_examples([])
        }
    
    logger.info(f"Analyzing {len(comments)} YouTube comments with LLM")
    
    # 1. First analyze sentiment if we have an API key
    sentiment_result = await analyze_sentiment(comments)
    
    # 2. Identify the most critical comments
    filtered_comments = comments
    if len(comments) > limit:
        try:
            # Try to identify the most critical comments
            critical_comments = await identify_critical_comments(comments, max_comments=limit)
            if critical_comments and len(critical_comments) > 0:
                filtered_comments = critical_comments
                logger.info(f"Identified {len(filtered_comments)} critical comments from {len(comments)} total")
            else:
                # If failed to identify, use the first 'limit' comments
                filtered_comments = comments[:limit]
                logger.warning(f"Failed to identify critical comments, using first {limit} comments")
        except Exception as e:
            logger.error(f"Error identifying critical comments: {e}")
            filtered_comments = comments[:limit]
    
    # 3. Generate response strategies
    strategies = await generate_response_strategies(filtered_comments)
    
    # 4. Generate example responses
    examples = await generate_example_responses(filtered_comments)
    
    # Create a comprehensive response
    result = {
        "sentiment": sentiment_result,
        "toxicity": {"toxic": 0, "severe_toxic": 0, "obscene": 0, "threat": 0, "insult": 0, "identity_hate": 0},
        "strategies": strategies,
        "example_comments": examples
    }
    
    logger.info(f"LLM analysis complete. Sentiment: {sentiment_result}, Strategies: {len(strategies) if isinstance(strategies, list) else 'text'}, Examples: {len(examples)}")
    
    return result

async def analyze_sentiment(comments: List[str]) -> Dict[str, int]:
    """
    Analyze sentiment of comments using LLM API
    
    Args:
        comments: List of comment strings
        
    Returns:
        Dictionary with counts of positive, neutral, and negative comments
    """
    if not API_KEY:
        logger.error("Cannot analyze sentiment: API key missing")
        return {"Positive": 0, "Neutral": len(comments), "Negative": 0}
    
    # If there are too many comments, select only a subset for analysis
    sample_size = min(50, len(comments))
    if len(comments) > sample_size:
        import random
        # Randomly select comments to ensure representative sampling
        sampled_comments = random.sample(comments, sample_size)
    else:
        sampled_comments = comments
    
    # Prepare prompt for the LLM
    comments_text = "\n".join([f"- {comment}" for comment in sampled_comments])
    prompt = f"""Analyze these YouTube comments and classify each one as Positive, Neutral, or Negative:

{comments_text}

Count the number of comments in each category and return ONLY a JSON object in this format:
{{
  "Positive": [number of positive comments],
  "Neutral": [number of neutral comments],
  "Negative": [number of negative comments]
}}

DO NOT add any explanation, introductory text, or other formatting.
"""
    
    system_message = """You are an expert sentiment analysis assistant. Classify comments based on these guidelines:
    
    - Positive: Contains praise, appreciation, excitement, or other positive sentiments.
    - Negative: Contains criticism, disappointment, anger, or other negative sentiments.
    - Neutral: Factual, questioning, or lacks clear positive or negative sentiment.
    
    Return ONLY a JSON object with the count in each category.
    """
    
    try:
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "max_tokens": 500
        }
        
        resp = _session.post(url=API_URL, data=json.dumps(payload), timeout=300)
        resp.raise_for_status()
        data = resp.json()
        
        # Check response structure
        if 'choices' not in data:
            logger.error(f"API response missing 'choices' key: {data}")
            return {"Positive": 0, "Neutral": len(comments), "Negative": 0}
            
        choices = data.get('choices', [])
        if not choices or len(choices) == 0:
            logger.error("API response choices list is empty")
            return {"Positive": 0, "Neutral": len(comments), "Negative": 0}
            
        first_choice = choices[0]
        if not isinstance(first_choice, dict):
            logger.error(f"choices[0] is not a dictionary type: {type(first_choice)}")
            return {"Positive": 0, "Neutral": len(comments), "Negative": 0}
            
        message = first_choice.get('message', {})
        if not isinstance(message, dict):
            logger.error(f"message is not a dictionary type: {type(message)}")
            return {"Positive": 0, "Neutral": len(comments), "Negative": 0}
            
        content = message.get('content', '')
        if not content:
            logger.error("No content in API response")
            return {"Positive": 0, "Neutral": len(comments), "Negative": 0}
            
        # Attempt to parse JSON
        try:
            sentiment_data = json.loads(content)
            # Ensure we have all required keys
            if "Positive" not in sentiment_data or "Neutral" not in sentiment_data or "Negative" not in sentiment_data:
                logger.error(f"JSON response missing required keys: {sentiment_data}")
                return {"Positive": 0, "Neutral": len(comments), "Negative": 0}
                
            # Check for valid numerical values
            if not all(isinstance(sentiment_data[key], int) for key in ["Positive", "Neutral", "Negative"]):
                logger.error(f"JSON response contains non-integer values: {sentiment_data}")
                return {"Positive": 0, "Neutral": len(comments), "Negative": 0}
                
            # Ensure total count doesn't exceed sample size
            total = sentiment_data["Positive"] + sentiment_data["Neutral"] + sentiment_data["Negative"]
            if total > sample_size:
                logger.error(f"Total sentiment count {total} exceeds sample size {sample_size}")
                # Adjust values to ensure correct total
                scale_factor = sample_size / total
                sentiment_data = {
                    "Positive": int(sentiment_data["Positive"] * scale_factor),
                    "Neutral": int(sentiment_data["Neutral"] * scale_factor),
                    "Negative": int(sentiment_data["Negative"] * scale_factor)
                }
                # Ensure the sum equals the sample size
                diff = sample_size - sum(sentiment_data.values())
                sentiment_data["Neutral"] += diff  # Add difference to Neutral category
                
            # If we analysed a sample, scale up to the full comment set
            if len(comments) > sample_size:
                scale_factor = len(comments) / sample_size
                sentiment_data = {
                    "Positive": int(sentiment_data["Positive"] * scale_factor),
                    "Neutral": int(sentiment_data["Neutral"] * scale_factor),
                    "Negative": int(sentiment_data["Negative"] * scale_factor)
                }
                # Ensure the sum equals the total comment count
                diff = len(comments) - sum(sentiment_data.values())
                sentiment_data["Neutral"] += diff  # Add difference to Neutral category
                
            return sentiment_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from API response: {e}")
            logger.error(f"Content was: {content}")
            return {"Positive": 0, "Neutral": len(comments), "Negative": 0}
            
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {e}")
        return {"Positive": 0, "Neutral": len(comments), "Negative": 0}

async def identify_critical_comments(comments: List[str], max_comments: int = 3) -> List[str]:
    """
    Identify the most toxic and harmful comments that need addressing.
    
    Args:
        comments: List of comment strings
        max_comments: Maximum number of critical comments to return
        
    Returns:
        List of the most toxic/harmful comments
    """
    if not API_KEY:
        logger.error("Cannot identify critical comments: API key missing")
        return []
    
    # Prepare prompt for the LLM
    comments_text = "\n".join([f"- {comment}" for comment in comments])
    prompt = f"""Analyse these YouTube comments and identify the {max_comments} most toxic, offensive or harmful ones:

{comments_text}

PRIORITISE comments that contain:
1. Personal attacks or insults
2. Hate speech, slurs, or discriminatory language
3. Severe negativity or hostility
4. Threatening or intimidating language
5. Harmful misinformation

IMPORTANT: Return ONLY the exact text of the {max_comments} most toxic comments, one per line.
DO NOT add any introductory text, summaries, or phrases like "The most toxic comments are:".
DO NOT number the comments or add any formatting.
ONLY return the raw comment text, exactly as provided in the input.
"""
    
    system_message = """You are an expert content moderation assistant specialising in identifying toxic content.
    
    Your primary task is to identify comments that are harmful, toxic, or potentially dangerous. Focus on comments that:
    - Contain personal attacks or abusive language
    - Include hate speech, slurs, or discriminatory content
    - Feature extreme negativity or hostility
    - Contain threatening language or intimidation
    - Spread harmful misinformation
    
    PRIORITISE the most toxic comments first, rather than merely critical ones.
    
    When presenting your findings, NEVER add introductory phrases or explanations.
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
        
        resp = _session.post(url=API_URL, data=json.dumps(payload), timeout=300)
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
                    "the most", "here are", "these are", "comments are", "identified", "response", 
                    "would require", "toxic", "critical", "negative", "harmful"
                ]):
                    continue
                filtered_comments.append(comment)
            
            # If filtering removed too much, use the original list
            if len(filtered_comments) < 1 and critical_comments:
                logger.warning("Filtering removed too many comments, using original list")
                filtered_comments = critical_comments
            
            if filtered_comments:
                # Validate that each returned comment appears in the original comments
                # This prevents hallucinated comments from being included
                valid_comments = []
                for comment in filtered_comments:
                    found = False
                    for original in comments:
                        if comment.strip() in original:
                            valid_comments.append(original)
                            found = True
                            break
                    if not found:
                        logger.warning(f"Comment not found in original list, possible hallucination: {comment}")
                
                if valid_comments:
                    # Limit to requested number
                    valid_comments = valid_comments[:max_comments]
                    return valid_comments
        
        # Fallback if failed to extract valid comments
        logger.warning("Failed to extract valid critical comments from LLM response")
        return comments[:min(max_comments, len(comments))]
    
    except Exception as e:
        logger.error(f"Error identifying critical comments: {e}")
        return comments[:min(max_comments, len(comments))]

async def generate_response_strategies(critical_comments: List[str]) -> str:
    """
    Generate response strategies for YouTube comments based on the most critical comments.
    
    Args:
        critical_comments: List of the most critical comments to address
        
    Returns:
        String with response strategies in plain text
    """
    if not API_KEY:
        logger.error("Cannot generate response strategies: API key missing")
        return "API key is missing, cannot generate response strategies."
    
    if not critical_comments:
        logger.warning("No critical comments provided to generate strategies")
        return generate_fallback_strategies([])
    
    # Format comments for prompt
    comments_text = "\n".join([f"- {comment}" for comment in critical_comments])
    
    # Create prompt for strategies
    prompt = f"""Based on these challenging YouTube comments, create 4-6 effective response strategies for the content creator:

{comments_text}

Create 4-6 specific strategies, each with a descriptive title followed by a brief explanation.
Format each strategy as: "Strategy Title: Brief explanation of the strategy."
Do NOT use bullet points, asterisks, dashes or any other list markers.
Focus on professional, positive, and constructive ways to engage with the comments.
Return ONLY the strategies with no introduction or conclusion.
"""
    
    system_message = """You are an expert in online community management and content creation.
    
    Your task is to help content creators respond effectively to comments.
    
    Format your response as plain text strategies with no bullet points or special characters.
    Each strategy should have a clear title followed by a brief explanation.
    For example:
    Acknowledge Positive Feedback: Thank viewers for their kind words and show appreciation for their support.
    Address Specific Points: Respond to individual comments that mention specific aspects of your content.
    
    DO NOT include any introduction, conclusion, bullet points, or special formatting.
    DO NOT use asterisks, dashes, or any list markers.
    ONLY provide the strategies as plain text, one per paragraph."""
    
    try:
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 800
        }
        
        resp = _session.post(url=API_URL, data=json.dumps(payload), timeout=300)
        resp.raise_for_status()
        data = resp.json()
        
        # Check if we have a valid response
        if 'choices' in data and data['choices'] and 'message' in data['choices'][0]:
            content = data['choices'][0]['message'].get('content', '')
            if content:
                # Clean up the response to remove any bullet points or formatting
                cleaned_content = content
                
                # Remove any bullet points or list markers
                cleaned_content = re.sub(r'^\s*[-•*]\s*', '', cleaned_content, flags=re.MULTILINE)
                
                # Remove numbers at the beginning of lines
                cleaned_content = re.sub(r'^\s*\d+\.\s*', '', cleaned_content, flags=re.MULTILINE)
                
                # If we have valid content after cleaning, return it
                if cleaned_content.strip():
                    return cleaned_content.strip()
        
        # If we couldn't parse a valid response, use fallback
        logger.warning("Failed to generate valid response strategies from LLM, using fallback")
        return generate_fallback_strategies(critical_comments)
        
    except Exception as e:
        logger.error(f"Error generating response strategies: {e}")
        return generate_fallback_strategies(critical_comments)

async def generate_example_responses(critical_comments: List[str]) -> List[Dict[str, str]]:
    """
    Generate example responses to critical YouTube comments.
    
    Args:
        critical_comments: List of critical comments to respond to
        
    Returns:
        List of dictionaries with 'comment' and 'response' keys
    """
    if not API_KEY:
        logger.error("Cannot generate example responses: API key missing")
        return generate_fallback_examples([])
    
    if not critical_comments:
        logger.warning("No critical comments provided to generate responses")
        return generate_fallback_examples([])
    
    # Create prompt for response examples
    examples = []
    for comment in critical_comments[:3]:  # Limit to 3 to avoid too large requests
        try:
            # Individual prompt for each comment to keep responses focused
            prompt = f"""As a YouTube content creator, draft a thoughtful, professional response to this comment:

"{comment}"

Your response should:
1. Be genuinely helpful and courteous
2. Address the specific concerns raised
3. Be conversational but professional
4. Avoid being defensive
5. Be 2-4 sentences maximum

Format your response as a JSON object with this structure:
{{
  "comment": "THE ORIGINAL COMMENT",
  "response": "YOUR SUGGESTED RESPONSE"
}}

Return ONLY the JSON object with no other text."""
            
            system_message = """You are an expert community manager for a professional content creator.
            
            Your task is to craft thoughtful, professional responses to YouTube comments that will:
            - Acknowledge the viewer's feedback
            - Address their concerns constructively
            - Maintain a positive brand image
            - Encourage continued engagement
            
            Return your response as a JSON object containing both the original comment and your proposed response."""
            
            payload = {
                "model": MODEL_NAME,
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                "response_format": {"type": "json_object"},
                "max_tokens": 500
            }
            
            resp = _session.post(url=API_URL, data=json.dumps(payload), timeout=300)
            resp.raise_for_status()
            data = resp.json()
            
            # Process response
            if 'choices' in data and data['choices'] and 'message' in data['choices'][0]:
                content = data['choices'][0]['message'].get('content', '')
                if content:
                    try:
                        # Parse JSON response
                        response_data = json.loads(content)
                        
                        # Validate the returned object has the correct structure
                        if 'comment' in response_data and 'response' in response_data:
                            # Ensure the original comment is preserved
                            response_data['comment'] = comment
                            examples.append(response_data)
                        else:
                            logger.warning(f"Invalid JSON structure in response: {response_data}")
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse JSON from response: {content}")
                        # Attempt to extract response from non-JSON content
                        if "Response:" in content:
                            try:
                                response_part = content.split("Response:", 1)[1].strip()
                                examples.append({
                                    "comment": comment,
                                    "response": response_part
                                })
                            except:
                                logger.warning("Failed to extract response from non-JSON content")
            
        except Exception as e:
            logger.error(f"Error generating response for comment '{comment[:30]}...': {e}")
    
    # If we got at least one valid example, return them
    if examples:
        return examples
    
    # Otherwise, use fallback examples
    logger.warning("Failed to generate any valid examples, using fallback")
    return generate_fallback_examples(critical_comments)

# Fallback function returning plain text without formatting
def generate_fallback_strategies(comments: List[str]) -> str:
    """Generate predefined response strategies in plain text"""
    return """Acknowledge the feedback without defensiveness: Thank viewers for taking time to comment and show appreciation for their engagement.

Focus on constructive elements: Address specific points made in comments while politely ignoring personal attacks or negativity.

Keep responses brief and positive: Maintain a professional tone and focus on being helpful rather than defensive.

Use feedback as opportunity for improvement: Mention how you'll consider their suggestions in future content.

Remember selective engagement is okay: Not every comment requires a response, especially purely negative ones that offer no constructive value."""

def generate_fallback_examples(comments: List[str]) -> List[Dict[str, str]]:
    """Generate predefined example responses in Australian English"""
    # Ensure we return useful examples even if no comments are provided
    if not comments:
        return [
            {
                "comment": "Your video was absolute rubbish, you clearly don't know what you're on about!",
                "response": "G'day! Thanks for watching and sharing your thoughts. I'm keen to improve - if you've got specific feedback, I'd be chuffed to hear more."
            },
            {
                "comment": "This makes no sense. You're just waffling on about nothing important.",
                "response": "Cheers for taking the time to watch, mate. I'm working on making my explanations clearer - if a specific part confused you, let me know!"
            },
            {
                "comment": "I can't believe you think this is good advice. It's completely wrong and misleading.",
                "response": "Thanks for your candid feedback. My advice comes from my experience, but I'm always open to different perspectives. What approach would you recommend instead?"
            }
        ]
    
    # Generate generic but reasonable responses for actual comments
    results = []
    for i, comment in enumerate(comments[:3]):  # Process at most 3 comments
        # Take first 100 chars of comment as preview
        preview = comment[:100] + "..." if len(comment) > 100 else comment
        
        # Choose different standard responses based on comment length
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
