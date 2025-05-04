#!/usr/bin/env python3
"""
Comprehensive backend API testing script
Tests the complete flow of all main backend services
"""
import os
import sys
import time
import json
import logging
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("backend-test")

# Default base URL - can be overridden with environment variable
BASE_URL = os.getenv("API_BASE", "https://api.tiezhu.org")

class BackendTestSuite:
    """Test suite for the backend API flow"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.test_results = []
        self.timeout = 30  # Default timeout for requests
        self.long_timeout = 120  # Longer timeout for analysis requests
        logger.info(f"Initializing test suite with base URL: {base_url}")
        
    def run_test(self, test_name: str, test_func, *args, **kwargs) -> bool:
        """Run a test and record the result"""
        start_time = time.time()
        logger.info(f"Running test: {test_name}")
        
        try:
            result = test_func(*args, **kwargs)
            success = True
            error_message = None
        except Exception as e:
            result = None
            success = False
            error_message = str(e)
            logger.error(f"Test failed: {test_name} - {error_message}")
        
        elapsed_time = time.time() - start_time
        
        # Record test result
        self.test_results.append({
            "test_name": test_name,
            "success": success,
            "error_message": error_message,
            "elapsed_time": elapsed_time,
            "timestamp": datetime.now().isoformat()
        })
        
        return success
    
    def get_url(self, path: str) -> str:
        """Get full URL for a given API path"""
        # Ensure path starts with /
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{self.base_url}{path}"
    
    def test_health_endpoint(self) -> Dict[str, Any]:
        """Test the health check endpoint"""
        response = requests.get(
            self.get_url("/api/health"),
            timeout=self.timeout
        )
        
        if response.status_code != 200:
            raise Exception(f"Health check failed with status code: {response.status_code}")
        
        data = response.json()
        if data.get("status") not in ["ok", "healthy"]:
            raise Exception(f"Health check returned non-healthy status: {data.get('status')}")
        
        logger.info(f"Health check successful: {data.get('status')}")
        return data
    
    def test_youtube_analyze(self, video_url: str = "https://www.youtube.com/watch?v=dQw4w9WgXcQ") -> Dict[str, Any]:
        """Test the YouTube analysis endpoint"""
        payload = {
            "video_url": video_url,
            "max_comments": 20  # Reduced comments for faster testing
        }
        
        response = requests.post(
            self.get_url("/api/youtube/analyze"),
            json=payload,
            timeout=self.long_timeout
        )
        
        if response.status_code != 200:
            raise Exception(f"YouTube analysis failed with status code: {response.status_code}")
        
        data = response.json()
        if "status" in data and data["status"] == "error":
            raise Exception(f"YouTube analysis returned error: {data.get('message')}")
        
        logger.info(f"YouTube analysis successful - returned data with keys: {list(data.keys())}")
        return data
    
    def test_get_comments(self, video_url: str = "https://www.youtube.com/watch?v=dQw4w9WgXcQ") -> Dict[str, Any]:
        """Test the endpoint for getting YouTube comments"""
        payload = {
            "video_url": video_url,
            "max_comments": 15
        }
        
        response = requests.post(
            self.get_url("/api/youtube/comments"),
            json=payload,
            timeout=self.timeout
        )
        
        if response.status_code != 200:
            raise Exception(f"Get comments failed with status code: {response.status_code}")
        
        data = response.json()
        if "status" in data and data["status"] == "error":
            raise Exception(f"Get comments returned error: {data.get('message')}")
            
        if "comments" not in data or not data["comments"]:
            raise Exception("No comments returned from API")
            
        logger.info(f"Successfully retrieved {len(data['comments'])} comments from YouTube")
        return data
    
    def test_nlp_process(self) -> Dict[str, Any]:
        """Test the NLP processing endpoint with sample comments"""
        # Use sample comments to avoid depending on the YouTube API
        sample_comments = [
            {"text": "This video is amazing!", "author": "TestUser1", "likes": 10},
            {"text": "I disagree with some points made in the video", "author": "TestUser2", "likes": 5},
            {"text": "Great content as always!", "author": "TestUser3", "likes": 8}
        ]
        
        payload = {
            "video_title": "Test Video",
            "comments": sample_comments
        }
        
        response = requests.post(
            self.get_url("/api/youtube/process_comments"),
            json=payload,
            timeout=self.long_timeout
        )
        
        if response.status_code != 200:
            raise Exception(f"NLP processing failed with status code: {response.status_code}")
        
        data = response.json()
        if "status" in data and data["status"] == "error":
            raise Exception(f"NLP processing returned error: {data.get('message')}")
            
        logger.info("NLP processing successful")
        return data
    
    def test_notes_endpoints(self) -> Dict[str, Any]:
        """Test the notes endpoints (create, list, update, delete)"""
        # First create a note
        create_payload = {
            "title": "Test Note",
            "content": "This is a test note created by the automated test script",
            "category": "testing"
        }
        
        create_response = requests.post(
            self.get_url("/api/notes"),
            json=create_payload,
            timeout=self.timeout
        )
        
        if create_response.status_code != 200:
            raise Exception(f"Note creation failed with status code: {create_response.status_code}")
        
        create_data = create_response.json()
        note_id = create_data.get("id")
        
        if not note_id:
            raise Exception("Note creation didn't return a note ID")
        
        logger.info(f"Successfully created test note with ID: {note_id}")
        
        # Get the list of notes to confirm it's there
        list_response = requests.get(
            self.get_url("/api/notes"),
            timeout=self.timeout
        )
        
        if list_response.status_code != 200:
            raise Exception(f"Note listing failed with status code: {list_response.status_code}")
        
        notes = list_response.json()
        
        if not any(note.get("id") == note_id for note in notes):
            raise Exception(f"Created note with ID {note_id} not found in notes listing")
        
        logger.info(f"Successfully verified note in listing")
        
        # Update the note
        update_payload = {
            "title": "Updated Test Note",
            "content": "This note has been updated by the test script",
            "category": "testing"
        }
        
        update_response = requests.put(
            self.get_url(f"/api/notes/{note_id}"),
            json=update_payload,
            timeout=self.timeout
        )
        
        if update_response.status_code != 200:
            raise Exception(f"Note update failed with status code: {update_response.status_code}")
        
        logger.info(f"Successfully updated test note")
        
        # Delete the note
        delete_response = requests.delete(
            self.get_url(f"/api/notes/{note_id}"),
            timeout=self.timeout
        )
        
        if delete_response.status_code != 200:
            raise Exception(f"Note deletion failed with status code: {delete_response.status_code}")
        
        logger.info(f"Successfully deleted test note")
        
        # Return success data
        return {"success": True, "note_id": note_id}
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests in the test suite"""
        logger.info(f"Starting complete backend test flow against {self.base_url}")
        
        self.run_test("Health Check", self.test_health_endpoint)
        self.run_test("Get Comments", self.test_get_comments)
        self.run_test("NLP Processing", self.test_nlp_process)
        self.run_test("Notes Flow", self.test_notes_endpoints)
        
        # YouTube analysis is last as it takes the longest
        self.run_test("YouTube Analysis", self.test_youtube_analyze)
        
        # Calculate summary statistics
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        logger.info(f"Test suite completed. Passed: {passed_tests}/{total_tests}, Failed: {failed_tests}/{total_tests}")
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": passed_tests / total_tests if total_tests > 0 else 0,
            "results": self.test_results
        }
    
    def print_summary(self) -> None:
        """Print a summary of test results"""
        if not self.test_results:
            logger.warning("No test results to summarize")
            return
        
        print("\n" + "="*50)
        print(f"BACKEND TEST SUMMARY FOR {self.base_url}")
        print("="*50)
        
        for i, result in enumerate(self.test_results, 1):
            status = "PASS" if result["success"] else "FAIL"
            print(f"{i}. {result['test_name']}: {status} ({result['elapsed_time']:.2f}s)")
            if not result["success"]:
                print(f"   Error: {result['error_message']}")
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        
        print("-"*50)
        print(f"Passed: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.1f}%)")
        print("="*50)


def main():
    """Main entry point for running the test suite"""
    # Check if a custom base URL was provided
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = BASE_URL
        
    # Create and run the test suite
    test_suite = BackendTestSuite(base_url)
    test_suite.run_all_tests()
    test_suite.print_summary()
    
    # Exit with error code if any tests failed
    sys.exit(0 if all(result["success"] for result in test_suite.test_results) else 1)


if __name__ == "__main__":
    main() 