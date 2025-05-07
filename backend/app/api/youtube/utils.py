import re
import logging

# Configure logger
logger = logging.getLogger(__name__)

def extract_video_id(url: str) -> str:
    """
    Extract YouTube video ID from a URL.
    
    Args:
        url: YouTube URL in various possible formats
        
    Returns:
        YouTube video ID or empty string if not found
    """
    if not url:
        return ""
    
    # Common patterns for YouTube URLs
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/v\/([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/user\/\w+\/watch\?v=([a-zA-Z0-9_-]{11})',
        r'youtube-nocookie\.com\/embed\/([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/verify_age\?.*next_url=.*%3Fv%3D([a-zA-Z0-9_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # If direct ID was provided (11 characters)
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url):
        return url
    
    logger.warning(f"Could not extract video ID from URL: {url}")
    return "" 