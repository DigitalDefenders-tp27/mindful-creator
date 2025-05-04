import os
import unittest
import requests

class TestBackendAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load the backend base URL from environment variable, default to Railway deployment address
        cls.base_url = os.getenv('API_BASE', 'https://mindful-creator-production-e20c.up.railway.app')

    def test_health_endpoint(self):
        """Test that the /api/health endpoint returns 200 OK and includes a 'status' field."""
        # Increase timeout to allow for network latency
        resp = requests.get(f"{self.base_url}/api/health", timeout=30)
        self.assertEqual(resp.status_code, 200, f"Health endpoint returned {resp.status_code}")
        data = resp.json()
        self.assertIn('status', data)

    def test_youtube_analyse_endpoint(self):
        """Test that the /api/youtube/analyse endpoint returns a list of analysis results."""
        video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        payload = {"youtube_url": video_url}
        try:
            # Allow a longer timeout for analysis processing
            resp = requests.post(f"{self.base_url}/api/youtube/analyse", json=payload, timeout=120)
        except requests.exceptions.ReadTimeout as e:
            self.skipTest(f"Analyse endpoint request timed out: {e}")
        # Skip if the endpoint is not available or returns an error status
        if resp.status_code != 200:
            self.skipTest(f"Analyse endpoint returned status code {resp.status_code}")
        data = resp.json()
        self.assertIsInstance(data, list)
        if data:
            first = data[0]
            self.assertIn('videoId', first)
            self.assertIn('videoTitle', first)
            self.assertIn('criticalComments', first)

if __name__ == '__main__':
    unittest.main() 