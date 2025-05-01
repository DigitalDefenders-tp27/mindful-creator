from fastapi import APIRouter, HTTPException
from typing import Dict
import json
import os
from pathlib import Path
import fcntl
import contextlib

router = APIRouter()

# File path for storing ratings
RATINGS_FILE = Path("data/activity_ratings.json")
LOCK_FILE = Path("data/activity_ratings.lock")

# Ensure the data directory exists
RATINGS_FILE.parent.mkdir(parents=True, exist_ok=True)

@contextlib.contextmanager
def file_lock():
    """Context manager for file locking."""
    with open(LOCK_FILE, 'w') as lock_file:
        try:
            # Acquire an exclusive lock
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
            yield
        finally:
            # Release the lock
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)

def load_ratings():
    """Load ratings from file."""
    if RATINGS_FILE.exists():
        with open(RATINGS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_ratings(ratings):
    """Save ratings to file."""
    with open(RATINGS_FILE, 'w') as f:
        json.dump(ratings, f, indent=2)

@router.get("/activities/{activity_type}/ratings-count")
async def get_ratings_count(activity_type: str):
    """Get the total number of ratings for a specific activity."""
    try:
        with file_lock():
            ratings = load_ratings()
            count = ratings.get(activity_type, 0)
            return {"count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/activities/submit-rating")
async def submit_rating(data: Dict):
    """Submit a rating for an activity."""
    try:
        activity = data.get("activity")
        rating = data.get("rating")
        
        if not activity or not rating:
            raise HTTPException(status_code=400, detail="Missing activity or rating")
        
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise HTTPException(status_code=400, detail="Rating must be an integer between 1 and 5")
        
        with file_lock():
            # Load current ratings
            ratings = load_ratings()
            
            # Increment the rating count for this activity
            if activity not in ratings:
                ratings[activity] = 0
            ratings[activity] += 1
            
            # Save updated ratings
            save_ratings(ratings)
        
        return {"success": True}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 