"""Client for interacting with the YouTube API to fetch video comments."""
import os
import logging
import asyncio
from typing import List, Optional
import googleapiclient.discovery
from googleapiclient.errors import HttpError

# Configure logger
logger = logging.getLogger(__name__)

class YouTubeClient:
    """Initialize the YouTube client with API key from environment variables"""
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.youtube = None
        
        if not self.api_key:
            logger.warning("YOUTUBE_API_KEY environment variable not set")
            return
            
        # Initialize the YouTube API client
        self.youtube = googleapiclient.discovery.build(
            "youtube", "v3", developerKey=self.api_key
        )
        logger.info("YouTube client initialized successfully")
    
    async def get_video_comments(self, video_id: str, max_comments: int = 100) -> List[str]:
        """
        Fetch comments from a YouTube video.
        
        Args:
            video_id: YouTube video ID
            max_comments: Maximum number of comments to fetch
            
        Returns:
            List of comment strings
        """
        if not self.youtube:
            logger.error("YouTube API client not initialized")
            return []
            
        comments = []
        try:
            next_page = None
            
            while len(comments) < max_comments:
                # Request comments from YouTube API using asyncio.to_thread
                resp = await asyncio.to_thread(
                    lambda: self.youtube.commentThreads()
                    .list(
                        part="snippet",
                        videoId=video_id,
                        textFormat="plainText",
                        maxResults=min(100, max_comments - len(comments)),
                        pageToken=next_page,
                    )
                    .execute()
                )
                
                # Extract comment text
                for item in resp.get("items", []):
                    text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                    comments.append(text)
                    
                # Check if there's another page
                next_page = resp.get("nextPageToken")
                if not next_page:
                    break
                    
            logger.info(f"Successfully fetched {len(comments)} comments for video {video_id}")
            return comments
            
        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            return []
        except Exception as e:
            logger.error(f"Error fetching YouTube comments: {str(e)}")
            return [] 