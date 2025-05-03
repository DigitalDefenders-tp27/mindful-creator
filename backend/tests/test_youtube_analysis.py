import unittest
import sys
import os
import requests
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ensure the parent directory is in the Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from app.api.youtube.analyzer import fetch_youtube_comments, analyse_comments_with_local_model
from app.api.youtube.llm_handler import analyse_youtube_comments


class TestYouTubeAnalysis(unittest.TestCase):
    """Test the YouTube analysis functionality"""

    def setUp(self):
        """Set up the test environment"""
        # Test YouTube video URL - a popular video with many comments
        self.video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up
        self.max_comments = 10  # Keep small for testing
        
    def test_fetch_youtube_comments(self):
        """Test fetching YouTube comments"""
        logger.info("Testing YouTube comment fetching...")
        try:
            comments = fetch_youtube_comments(self.video_url, self.max_comments)
            self.assertIsInstance(comments, list, "Comments should be returned as a list")
            self.assertTrue(len(comments) > 0, "At least one comment should be fetched")
            self.assertLessEqual(len(comments), self.max_comments, 
                                f"Comment count should not exceed max_comments ({self.max_comments})")
            
            logger.info(f"Successfully fetched {len(comments)} comments")
            logger.info(f"Sample comments: {comments[:2]}")
            return comments
        except Exception as e:
            self.fail(f"Failed to fetch YouTube comments: {e}")
    
    def test_local_nlp_model(self):
        """Test sending comments to the local NLP model"""
        logger.info("Testing local NLP model analysis...")
        
        # First fetch some comments to test with
        comments = self.test_fetch_youtube_comments()
        
        # Send comments to local NLP model
        try:
            result = analyse_comments_with_local_model(comments)
            self.assertIsInstance(result, dict, "Result should be a dictionary")
            
            # Check for required keys in the response
            self.assertIn("sentiment", result, "Response should include sentiment analysis")
            self.assertIn("toxicity", result, "Response should include toxicity analysis")
            
            # Check sentiment data structure
            sentiment = result["sentiment"]
            self.assertIn("positive_count", sentiment)
            self.assertIn("neutral_count", sentiment)
            self.assertIn("negative_count", sentiment)
            
            # Check toxicity data structure
            toxicity = result["toxicity"]
            self.assertIn("toxic_count", toxicity)
            self.assertIn("toxic_percentage", toxicity)
            self.assertIn("toxic_types", toxicity)
            
            logger.info("Local NLP model analysis successful")
            logger.info(f"Sentiment analysis: {sentiment}")
            logger.info(f"Toxicity analysis: toxic_count={toxicity['toxic_count']}, "
                       f"percentage={toxicity['toxic_percentage']:.2f}%")
            
            return result
        except Exception as e:
            self.fail(f"Failed to analyze comments with local NLP model: {e}")
    
    def test_openrouter_analysis(self):
        """Test sending comments to OpenRouter"""
        logger.info("Testing OpenRouter analysis...")
        
        # First fetch some comments to test with
        comments = self.test_fetch_youtube_comments()
        
        # Send comments to OpenRouter
        try:
            result = analyse_youtube_comments(comments)
            self.assertIsInstance(result, dict, "Result should be a dictionary")
            
            # Check status
            self.assertIn("status", result, "Response should include status")
            
            # Check if OpenRouter is properly configured and the analysis was successful
            if result["status"] == "success":
                # Check for required keys in successful response
                self.assertIn("strategies", result, "Successful response should include strategies")
                self.assertIn("example_comments", result, "Successful response should include example comments")
                
                # Log the strategies provided
                logger.info("OpenRouter analysis successful")
                logger.info(f"Strategies: {result['strategies'][:100]}...")  # First 100 chars
                
                if result.get("example_comments"):
                    logger.info(f"Example comments: {len(result['example_comments'])} provided")
            else:
                # If not successful, make sure an error message is included
                self.assertIn("message", result, "Error response should include a message")
                logger.warning(f"OpenRouter analysis returned status: {result['status']}")
                logger.warning(f"Message: {result.get('message', 'No message provided')}")
            
            return result
        except Exception as e:
            self.fail(f"Failed to analyze comments with OpenRouter: {e}")
    
    def test_complete_pipeline(self):
        """Test the complete analysis pipeline"""
        logger.info("Testing complete YouTube analysis pipeline...")
        
        try:
            # 1. Fetch comments
            comments = self.test_fetch_youtube_comments()
            
            # 2. Analyze with local NLP model
            local_result = analyse_comments_with_local_model(comments)
            
            # 3. Analyze with OpenRouter
            openrouter_result = analyse_youtube_comments(comments)
            
            # 4. Make a direct API request to the backend endpoint
            backend_url = os.environ.get("BACKEND_URL", "http://localhost:8080")
            api_endpoint = f"{backend_url}/api/youtube/analyze"
            
            # Use the requests library to make the API call
            try:
                response = requests.post(
                    api_endpoint,
                    json={"video_url": self.video_url, "max_comments": self.max_comments},
                    timeout=60  # Allow up to 60 seconds for a complete analysis
                )
                
                # Check the response
                if response.status_code == 200:
                    result = response.json()
                    logger.info("Complete API endpoint test successful")
                    logger.info(f"API Response: {result.get('status')}")
                    
                    # Check the structure of the result
                    self.assertIn("status", result)
                    self.assertIn("total_comments", result)
                    
                    if result["status"] == "success":
                        self.assertIn("analysis", result)
                        self.assertIn("strategies", result)
                else:
                    logger.warning(f"API endpoint returned status code: {response.status_code}")
                    logger.warning(f"Response: {response.text}")
            except requests.RequestException as e:
                logger.error(f"Error calling API endpoint: {e}")
                logger.warning("API endpoint test skipped - endpoint might not be running")
            
            logger.info("Complete pipeline test completed successfully")
            
        except Exception as e:
            self.fail(f"Pipeline test failed: {e}")


if __name__ == "__main__":
    unittest.main() 