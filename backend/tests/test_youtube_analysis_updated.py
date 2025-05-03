import unittest
import sys
import os
import requests
import logging
import json
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ensure the parent directory is in the Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import the necessary modules
from app.api.youtube.analyzer import extract_video_id, fetch_youtube_comments, analyse_comments_with_local_model
from app.api.youtube.llm_handler import analyse_youtube_comments


class TestYouTubeAnalysis(unittest.TestCase):
    """Test the YouTube analysis functionality with the updated backend"""

    def setUp(self):
        """Set up the test environment"""
        # Test YouTube video URL - a popular video with many comments
        self.video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up
        self.max_comments = 20  # Keep small for testing
        self.video_id = extract_video_id(self.video_url)
        self.backend_url = os.environ.get("BACKEND_URL", "http://localhost:8000")
        
        # Check if model is loaded
        self.model_loaded = os.environ.get("MODEL_LOADED", "false").lower() == "true"
        logger.info(f"Model loaded status: {self.model_loaded}")
        
    def test_extract_video_id(self):
        """Test extracting video ID from YouTube URL"""
        logger.info("Testing video ID extraction...")
        self.assertEqual(self.video_id, "dQw4w9WgXcQ", "Video ID extraction failed")
        logger.info(f"Successfully extracted video ID: {self.video_id}")
    
    def test_fetch_comments(self):
        """Test fetching YouTube comments with the new API"""
        logger.info("Testing YouTube comment fetching...")
        try:
            # Test with the video URL
            comments = fetch_youtube_comments(self.video_url, self.max_comments)
            self.assertIsInstance(comments, list, "Comments should be returned as a list")
            self.assertTrue(len(comments) > 0, "At least one comment should be fetched")
            self.assertLessEqual(len(comments), self.max_comments, 
                                f"Comment count should not exceed max_comments ({self.max_comments})")
            
            logger.info(f"Successfully fetched {len(comments)} comments")
            for i, comment in enumerate(comments[:3]):
                preview = str(comment)[:100] + "..." if len(str(comment)) > 100 else str(comment)
                logger.info(f"Comment {i+1}: {preview}")
            return comments
        except Exception as e:
            self.fail(f"Failed to fetch YouTube comments: {e}")
    
    def test_local_analysis(self):
        """Test analyzing comments with the local model"""
        logger.info("Testing local analysis model...")
        
        # First fetch some comments to test with
        comments = self.test_fetch_comments()
        
        # Analyze with local model
        try:
            result = analyse_comments_with_local_model(comments)
            self.assertIsInstance(result, dict, "Result should be a dictionary")
            
            # Check if we got a note about model not being loaded
            if "note" in result and "model not loaded" in result["note"].lower():
                logger.warning(f"Note: {result['note']}")
                self.assertFalse(self.model_loaded, "Model should be reported as not loaded")
            
            # Check for required keys in the response
            self.assertIn("sentiment", result, "Response should include sentiment analysis")
            self.assertIn("toxicity", result, "Response should include toxicity analysis")
            
            # Log the analysis results
            logger.info(f"Sentiment analysis: {json.dumps(result['sentiment'], indent=2)}")
            logger.info(f"Toxicity analysis: {json.dumps(result['toxicity'], indent=2)}")
            
            return result
        except Exception as e:
            self.fail(f"Failed to analyze comments with local model: {e}")
    
    def test_analyse_api_endpoint(self):
        """Test the /analyse API endpoint"""
        logger.info(f"Testing /analyse API endpoint at {self.backend_url}...")
        
        api_endpoint = f"{self.backend_url}/api/youtube/analyse"
        
        try:
            # Prepare the request payload
            payload = {
                "youtube_url": self.video_url,
                "limit": self.max_comments,
                "llm_enabled": True
            }
            
            logger.info(f"Sending request to {api_endpoint} with payload: {payload}")
            
            # Make the API request
            response = requests.post(
                api_endpoint,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30  # 30 second timeout
            )
            
            # Check response status
            self.assertEqual(response.status_code, 200, f"API request failed with status {response.status_code}: {response.text}")
            
            # Parse the response
            result = response.json()
            logger.info(f"API response status code: {response.status_code}")
            logger.info(f"API response: {json.dumps(result, indent=2)}")
            
            # Validate the response format
            self.assertIn("video_id", result, "Response should include video_id")
            self.assertIn("analysis", result, "Response should include analysis data")
            
            # Check model_status field
            if "model_status" in result:
                logger.info(f"Model status reported by API: {result['model_status']}")
                if result["model_status"] == "not_loaded":
                    self.assertIn("message", result, "Response should include a message when model is not loaded")
            
            # If LLM is enabled, check if llm_status is included
            if "llm_status" in result:
                logger.info(f"LLM status: {result['llm_status']}")
            
            return result
        except requests.RequestException as e:
            self.fail(f"Failed to call API endpoint: {e}")
    
    def test_api_response_times(self):
        """Test API response times with different payload sizes"""
        logger.info("Testing API response times with different payload sizes...")
        
        api_endpoint = f"{self.backend_url}/api/youtube/analyse"
        
        # Test with different comment limits
        limits = [10, 50, 100]
        results = {}
        
        for limit in limits:
            try:
                logger.info(f"Testing with limit={limit}...")
                
                # Prepare the request with LLM disabled for faster responses
                payload = {
                    "youtube_url": self.video_url,
                    "limit": limit,
                    "llm_enabled": False
                }
                
                # Make the API request and measure time
                import time
                start_time = time.time()
                
                response = requests.post(
                    api_endpoint,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=60
                )
                
                elapsed_time = time.time() - start_time
                
                # Store results
                results[limit] = {
                    "status_code": response.status_code,
                    "elapsed_time": elapsed_time,
                    "success": response.status_code == 200
                }
                
                logger.info(f"Limit={limit}: Response time={elapsed_time:.2f}s, Status={response.status_code}")
                
                # Check if successful
                if response.status_code == 200:
                    result = response.json()
                    if "analysis" in result and "video_id" in result:
                        results[limit]["video_id"] = result["video_id"]
                        if "model_status" in result:
                            results[limit]["model_status"] = result["model_status"]
                
            except requests.RequestException as e:
                logger.error(f"Error with limit={limit}: {e}")
                results[limit] = {
                    "status_code": None,
                    "elapsed_time": None,
                    "success": False,
                    "error": str(e)
                }
        
        # Log summary
        logger.info("\nAPI Response Time Summary:")
        logger.info(f"{'Limit':<10} {'Time (s)':<15} {'Status':<10} {'Success':<10}")
        for limit, data in results.items():
            time_str = f"{data['elapsed_time']:.2f}" if data['elapsed_time'] else "N/A"
            logger.info(f"{limit:<10} {time_str:<15} {data.get('status_code', 'N/A'):<10} {data['success']}")
        
        # Verify at least one request was successful
        self.assertTrue(any(data['success'] for data in results.values()),
                      "At least one API request should be successful")
        
        return results


if __name__ == "__main__":
    unittest.main() 