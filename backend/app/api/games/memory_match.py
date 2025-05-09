from fastapi import APIRouter, Depends, HTTPException, Query
import pandas as pd
import random
import os
import glob
from typing import List, Dict, Optional

router = APIRouter()

# Path to the meme dataset
MEME_DATASET_PATH = "backend/datasets/meme"
# Path to public meme directory
PUBLIC_MEME_PATH = "frontend/public/memes"

def ensure_meme_directory_exists():
    """Ensure that the meme directory exists."""
    if not os.path.exists(MEME_DATASET_PATH):
        os.makedirs(MEME_DATASET_PATH, exist_ok=True)
        # Create a README file to explain the directory purpose
        with open(os.path.join(MEME_DATASET_PATH, "README.md"), "w") as f:
            f.write("# Meme Dataset Directory\n\nThis directory contains meme images from the Memotion dataset for the memory match game.")

def get_meme_data() -> pd.DataFrame:
    """
    Load the meme dataset from a CSV file.
    Falls back to the sample dataset if the full dataset is not available.
    """
    # Ensure directory exists
    ensure_meme_directory_exists()
    
    # Try to load the full dataset
    full_dataset_path = os.path.join(MEME_DATASET_PATH, "memotion_dataset.csv")
    
    # Check for sample dataset if full dataset doesn't exist
    sample_dataset_path = "backend/datasets/memotion_sample.csv"
    
    # Load the dataset
    if os.path.exists(full_dataset_path):
        try:
            return pd.read_csv(full_dataset_path)
        except Exception as e:
            print(f"Error loading full dataset: {e}")
    
    # Try sample dataset as fallback
    if os.path.exists(sample_dataset_path):
        try:
            return pd.read_csv(sample_dataset_path)
        except Exception as e:
            print(f"Error loading sample dataset: {e}")
            
    # If both fail, return an empty DataFrame with the expected columns
    return pd.DataFrame({
        'image_name': [], 
        'text_corrected': [], 
        'overall_sentiment': [],
        'humour': [],
        'sarcasm': [],
        'offensive': [],
        'motivational': []
    })

@router.get("/memory-match")
async def get_memes_for_memory_match(
    level: int = Query(1, description="Game level: 1 (5 pairs) or 2 (25 pairs)")
) -> Dict:
    """
    Get random memes for the memory match game.
    
    Args:
        level: Game level (1 or 2)
    
    Returns:
        Dict containing meme information for the game
    """
    # Validate level
    if level not in [1, 2]:
        raise HTTPException(status_code=400, detail="Level must be 1 or 2")
    
    # Number of unique memes to fetch (level 1: 5 memes, level 2: 25 memes)
    num_memes = 5 if level == 1 else 25
    
    # Load the dataset
    df = get_meme_data()
    
    # Check if the dataset is empty
    if df.empty:
        raise HTTPException(status_code=404, detail="Meme dataset not found")
    
    # Ensure we have required columns
    required_columns = ['image_name', 'text_corrected', 'overall_sentiment']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise HTTPException(
            status_code=500, 
            detail=f"Dataset is missing required columns: {missing_columns}"
        )
    
    # Randomly select memes
    selected_memes = []
    
    # If dataset has fewer rows than required, use them all
    if len(df) <= num_memes:
        selected_indices = list(range(len(df)))
    else:
        selected_indices = random.sample(range(len(df)), num_memes)
    
    for idx in selected_indices:
        row = df.iloc[idx]
        
        # Extract available sentiment data
        sentiment_data = {
            'overall': row.get('overall_sentiment', 'neutral'),
            'humour': row.get('humour', 'unknown'),
            'sarcasm': row.get('sarcasm', 'unknown'),
            'offensive': row.get('offensive', 'unknown'),
            'motivational': row.get('motivational', 'unknown')
        }
        
        meme = {
            'id': int(idx),  # Use DataFrame index as ID
            'image_name': row['image_name'],
            'text': row.get('text_corrected', ''),
            'sentiment': sentiment_data,
            'image_path': f"/memes/{row['image_name']}" if 'image_name' in row else None
        }
        selected_memes.append(meme)
    
    return {
        "level": level,
        "memes": selected_memes
    }

@router.get("/scan-memes")
async def scan_available_memes() -> List[str]:
    """
    Scan for available meme images in the public directory.
    
    Returns:
        List of image filenames found in the public memes directory
    """
    all_meme_paths = []
    
    # Check the main public meme directory
    if os.path.exists(PUBLIC_MEME_PATH):
        for ext in ['jpg', 'jpeg', 'png', 'gif']:
            pattern = os.path.join(PUBLIC_MEME_PATH, f"*.{ext}")
            all_meme_paths.extend(glob.glob(pattern))
    
    # Always include the fallback test meme directory if we're in development
    test_meme_paths = []
    test_dir = "backend/datasets/test_memes"
    if os.path.exists(test_dir):
        for ext in ['jpg', 'jpeg', 'png', 'gif']:
            pattern = os.path.join(test_dir, f"*.{ext}")
            test_meme_paths.extend(glob.glob(pattern))
    
    # Extract just the filenames without full paths
    public_meme_files = [os.path.basename(p) for p in all_meme_paths]
    test_meme_files = [os.path.basename(p) for p in test_meme_paths]
    
    # Combine unique filenames from both sources
    all_meme_files = list(set(public_meme_files + test_meme_files))
    
    # Log what we found
    print(f"Found {len(all_meme_files)} unique meme files across all directories")
    
    return all_meme_files 