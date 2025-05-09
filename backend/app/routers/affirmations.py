from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import random
import os
import json

router = APIRouter(
    prefix="/affirmations",
    tags=["affirmations"],
)

# Path to the affirmations data file
AFFIRMATIONS_FILE = os.path.join("data", "affirmations.json")

# Default affirmations in case the file doesn't exist
DEFAULT_AFFIRMATIONS = [
    "I am enough just as I am.",
    "Today, I choose to be kind to myself.",
    "I embrace my imperfections with love and acceptance.",
    "I am deserving of happiness and good things.",
    "I trust my journey, even when the path is unclear.",
    "My potential to succeed is infinite.",
    "I have the power to create positive change in my life.",
    "I am grateful for all that I have in this moment.",
    "Today, I focus on what I can control.",
    "I am growing and evolving every day."
]

def get_affirmations() -> List[str]:
    """Load affirmations from the JSON file, or return defaults if file doesn't exist"""
    try:
        if os.path.exists(AFFIRMATIONS_FILE):
            with open(AFFIRMATIONS_FILE, 'r') as f:
                data = json.load(f)
                return data.get("affirmations", DEFAULT_AFFIRMATIONS)
        return DEFAULT_AFFIRMATIONS
    except Exception as e:
        print(f"Error loading affirmations: {e}")
        return DEFAULT_AFFIRMATIONS

@router.get("/")
async def get_all_affirmations() -> Dict[str, List[str]]:
    """Get all available affirmations"""
    return {"affirmations": get_affirmations()}

@router.get("/random")
async def get_random_affirmation() -> Dict[str, str]:
    """Get a random affirmation"""
    affirmations = get_affirmations()
    
    if not affirmations:
        raise HTTPException(status_code=404, detail="No affirmations available")
    
    random_affirmation = random.choice(affirmations)
    return {"affirmation": random_affirmation} 