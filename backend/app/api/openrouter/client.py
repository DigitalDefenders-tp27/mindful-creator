import os
import json
import logging
import requests
from typing import List, Dict, Any, Optional

from app.api.utils.logger import setup_logger

# Setup logger
logger = setup_logger('openrouter_client')

class OpenRouterClient:
    """Client for interacting with the OpenRouter API"""
    
    def __init__(self):
        """Initialize the OpenRouter client with API key from environment variables"""
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-prover-v2:free")
        
        if not self.api_key:
            logger.warning("OPENROUTER_API_KEY environment variable not set")
    
    def analyze_comments(self, comments: List[Dict[str, Any]], video_url: str) -> Optional[Dict[str, Any]]:
        """
        Analyze a list of YouTube comments using the OpenRouter API.
        
        Args:
            comments: List of comment dictionaries
            video_url: URL of the YouTube video
            
        Returns:
            Dictionary containing sentiment analysis, response strategies and example responses
        """
        if not self.api_key:
            logger.error("Cannot analyze comments: OpenRouter API key not set")
            return None
            
        try:
            # Extract comment texts
            comment_texts = [c["text"] for c in comments]
            
            # Prepare the prompt for the OpenRouter API
            prompt = self._prepare_analysis_prompt(comment_texts, video_url)
            
            # Send request to OpenRouter
            response = self._send_request(prompt)
            
            if not response:
                logger.warning("OpenRouter analysis returned empty response")
                return None
                
            # Process and structure the response
            return self._process_analysis_response(response)
            
        except Exception as e:
            logger.error(f"Error in OpenRouter comment analysis: {str(e)}")
            return None
    
    def single_comment_analysis(self, comment: str) -> str:
        """
        Analyze a single comment and generate a response suggestion.
        
        Args:
            comment: The comment text to analyze
            
        Returns:
            String containing the suggested response
        """
        if not self.api_key:
            logger.error("Cannot analyze comment: OpenRouter API key not set")
            return "Error: OpenRouter API key not configured"
            
        try:
            # Prepare the prompt for responding to a single comment
            prompt = f"""
                As a content creator responding to this YouTube comment, how would you respond professionally and positively?
                
                Comment: {comment}
                
                Please write a response that is:
                - Professional and courteous
                - Appreciative of feedback
                - Authentic and personal
                - Engaging but concise
                
                Response:
            """
            
            # Send request to OpenRouter
            response = self._send_request(prompt)
            
            if not response:
                return "Unable to generate a response at this time."
                
            # Return the text response
            return response
            
        except Exception as e:
            logger.error(f"Error in single comment analysis: {str(e)}")
            return f"Error generating response: {str(e)}"
    
    def _prepare_analysis_prompt(self, comments: List[str], video_url: str) -> str:
        """Prepare the prompt for YouTube comment analysis"""
        comments_text = "\n\n".join([f"Comment {i+1}: {comment}" for i, comment in enumerate(comments)])
        
        prompt = f"""
            You are an expert social media analyst helping a YouTube content creator understand and respond to their audience.
            
            I'll provide you with comments from this video: {video_url}
            
            Please analyze these comments and provide:
            
            1. SENTIMENT ANALYSIS: Count how many comments are positive, negative, or neutral.
            
            2. RESPONSE STRATEGIES: Provide 4-6 bullet points on how to engage with these commenters effectively.
            
            3. EXAMPLE RESPONSES: For 3-5 different comments, suggest a thoughtful response the creator could give.
            
            Here are the comments:
            
            {comments_text}
            
            FORMAT YOUR RESPONSE AS JSON with the following structure:
            {{
                "sentiment": {{
                    "Positive": number,
                    "Neutral": number,
                    "Negative": number
                }},
                "strategies": "• Strategy 1\\n• Strategy 2\\n• etc",
                "example_comments": [
                    {{
                        "comment": "original comment text",
                        "response": "your suggested response"
                    }},
                    ...
                ]
            }}
        """
        
        return prompt
    
    def _send_request(self, prompt: str) -> Optional[str]:
        """Send a request to the OpenRouter API and return the response text"""
        if not self.api_key:
            logger.error("Cannot send request: OpenRouter API key not set")
            return None
            
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
            
            logger.info(f"Sending request to OpenRouter API using model: {self.model}")
            response = requests.post(self.base_url, headers=headers, json=data)
            
            if response.status_code != 200:
                logger.error(f"OpenRouter API error: Status {response.status_code}, {response.text}")
                return None
                
            response_data = response.json()
            
            if not response_data or "choices" not in response_data or not response_data["choices"]:
                logger.warning("OpenRouter API returned empty choices")
                return None
                
            # Extract the response content
            response_text = response_data["choices"][0]["message"]["content"]
            logger.info("Received response from OpenRouter API")
            
            return response_text
            
        except Exception as e:
            logger.error(f"Error in OpenRouter API request: {str(e)}")
            return None
    
    def _process_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """Process and structure the response from OpenRouter API"""
        try:
            # Try to extract JSON from the response
            json_part = response_text
            
            # Check if response contains a markdown JSON block
            if "```json" in response_text:
                json_part = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                # Extract content from any markdown code block
                json_part = response_text.split("```")[1].split("```")[0].strip()
            
            # Parse the JSON
            result = json.loads(json_part)
            logger.info("Successfully parsed JSON response from OpenRouter")
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing OpenRouter response: {str(e)}")
            logger.debug(f"Raw response: {response_text[:500]}...")
            
            # Return a minimal structure with the raw response
            return {
                "sentiment": {"Positive": 0, "Neutral": 0, "Negative": 0},
                "strategies": "• Thank users for their feedback\n• Respond promptly to questions\n• Be authentic in your responses\n• Stay professional even with negative comments",
                "example_comments": [],
                "raw_response": response_text[:1000]  # Include truncated raw response for debugging
            } 