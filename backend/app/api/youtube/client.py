import os
import re
import logging
import googleapiclient.discovery
from urllib.parse import urlparse, parse_qs
from typing import List, Dict, Any, Optional

from app.api.utils.logger import setup_logger

# Setup logger
logger = setup_logger('youtube_client')

class YouTubeClient:
    """Client for interacting with the YouTube API to fetch video comments"""
    
    def __init__(self):
        """Initialize the YouTube client with API key from environment variables"""
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.youtube = None
        
        if not self.api_key:
            logger.warning("YOUTUBE_API_KEY environment variable not set")
        else:
            # Initialize the YouTube API client
            self.youtube = googleapiclient.discovery.build(
                "youtube", "v3", developerKey=self.api_key
            )
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """
        Extract the video ID from a YouTube URL.
        
        Args:
            url: YouTube video URL
            
        Returns:
            Video ID if found, None otherwise
        """
        # Handle mobile links (youtu.be)
        if "youtu.be" in url:
            return url.split("/")[-1].split("?")[0]
            
        # Handle full youtube.com links
        parsed_url = urlparse(url)
        if parsed_url.netloc in ["www.youtube.com", "youtube.com"]:
            if parsed_url.path == "/watch":
                # Handle watch URLs
                query_params = parse_qs(parsed_url.query)
                if "v" in query_params:
                    return query_params["v"][0]
                    
        # Handle embedded and shortened URLs
        youtube_id_match = re.search(r"(?:embed/|v=|vi=|/v/|youtu\.be/|/embed/|/v/|vi/)([^?&\n]+)", url)
        if youtube_id_match:
            return youtube_id_match.group(1)
            
        return None
    
    def get_video_comments(self, url: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve comments from a YouTube video.
        
        Args:
            url: YouTube video URL
            limit: Maximum number of comments to retrieve
            
        Returns:
            List of comment dictionaries with author and text information
        """
        if not self.youtube:
            logger.error("YouTube API client not initialized")
            return []
            
        video_id = self.extract_video_id(url)
        
        if not video_id:
            logger.error(f"Could not extract video ID from URL: {url}")
            return []
            
        try:
            # Request comments from YouTube API
            logger.info(f"Fetching up to {limit} comments for video ID: {video_id}")
            
            # Get first page of comments
            response = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=min(limit, 100),  # API limit is 100 per request
                textFormat="plainText",
                order="relevance"  # Get most relevant comments
            ).execute()
            
            # Extract comment data
            comments = []
            for item in response.get("items", []):
                snippet = item["snippet"]["topLevelComment"]["snippet"]
                comments.append({
                    "author": snippet["authorDisplayName"],
                    "text": snippet["textDisplay"],
                    "like_count": snippet["likeCount"],
                    "published_at": snippet["publishedAt"]
                })
                
                if len(comments) >= limit:
                    break
            
            # Get more pages if needed and available
            while (len(comments) < limit and 
                  "nextPageToken" in response and 
                  response["nextPageToken"]):
                next_page_token = response["nextPageToken"]
                response = self.youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=min(limit - len(comments), 100),
                    pageToken=next_page_token,
                    textFormat="plainText"
                ).execute()
                
                for item in response.get("items", []):
                    snippet = item["snippet"]["topLevelComment"]["snippet"]
                    comments.append({
                        "author": snippet["authorDisplayName"],
                        "text": snippet["textDisplay"],
                        "like_count": snippet["likeCount"],
                        "published_at": snippet["publishedAt"]
                    })
                    
                    if len(comments) >= limit:
                        break
            
            logger.info(f"Retrieved {len(comments)} comments for video ID: {video_id}")
            return comments
            
        except Exception as e:
            logger.error(f"Error fetching YouTube comments: {str(e)}")
            return [] 