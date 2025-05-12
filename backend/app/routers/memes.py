from fastapi import APIRouter, HTTPException, Path, Response, Query
from fastapi.responses import FileResponse
import pandas as pd
import os
from typing import List, Dict, Any, Optional
import random
import glob

router = APIRouter(
    prefix="/memes",
    tags=["memes"],
)

# Path to the meme dataset
MEME_DIR = os.path.join("datasets", "meme")
MEME_SAMPLE_CSV = os.path.join(MEME_DIR, "memotion_sample.csv")
MEME_IMAGES_DIR = os.path.join(MEME_DIR, "memotion_dataset_7k", "images")

def get_meme_data():
    """Load meme data from the sample CSV file"""
    try:
        if os.path.exists(MEME_SAMPLE_CSV):
            return pd.read_csv(MEME_SAMPLE_CSV)
        else:
            return pd.DataFrame()
    except Exception as e:
        print(f"Error loading meme data: {e}")
        return pd.DataFrame()

def find_meme_files(count: int = 25) -> List[Dict[str, Any]]:
    """Find actual meme files in the dataset directory"""
    if not os.path.exists(MEME_IMAGES_DIR):
        print(f"Error: Images directory not found at {MEME_IMAGES_DIR}")
        return []
    
    print(f"Looking for image files in: {MEME_IMAGES_DIR}")
    
    # Get a list of all image files in the directory
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.JPG', '*.JPEG', '*.PNG', '*.GIF']:
        pattern = os.path.join(MEME_IMAGES_DIR, ext)
        found = glob.glob(pattern)
        print(f"Found {len(found)} files with pattern: {pattern}")
        image_files.extend(found)
    
    print(f"Total image files found: {len(image_files)}")
    
    # If we found files, use them
    if image_files:
        # Get a random sample
        if len(image_files) > count:
            selected_files = random.sample(image_files, count)
            print(f"Selected {len(selected_files)} random files from {len(image_files)}")
        else:
            selected_files = image_files
            print(f"Using all {len(selected_files)} available files")
        
        # Convert to records
        memes = []
        for i, file_path in enumerate(selected_files):
            image_name = os.path.basename(file_path)
            memes.append({
                "id": i,
                "image_name": image_name,
                "text": f"Meme {i+1}",
                "humour": random.choice(["not_funny", "funny", "very_funny"]),
                "sarcasm": random.choice(["not_sarcastic", "general", "twisted_meaning"]),
                "offensive": random.choice(["not_offensive", "slight", "very_offensive"]),
                "motivational": random.choice(["motivational", "not_motivational"]),
                "overall_sentiment": random.choice(["negative", "neutral", "positive"])
            })
        
        print(f"Created {len(memes)} meme records from real image files")
        return memes
    
    print("No image files found in the dataset directory")
    return []

@router.get("/")
async def get_memes(count: Optional[int] = Query(25, description="Number of memes to return")) -> List[Dict[str, Any]]:
    """Get a list of memes for the memory match game"""
    df = get_meme_data()
    
    if df.empty:
        # If sample data is not available, try to generate it from the full dataset
        try:
            full_dataset_path = os.path.join(MEME_DIR, "memotion_dataset_7k", "labels.csv")
            if os.path.exists(full_dataset_path):
                # Load the full dataset
                df_full = pd.read_csv(full_dataset_path)
                # Sample a subset for the game
                df = df_full.sample(min(count, len(df_full)))
                print(f"Generated sample dataset with {len(df)} records from full dataset")
            else:
                print(f"Full dataset not found at {full_dataset_path}")
                
                # Try to use actual files instead
                memes = find_meme_files(count)
                if memes:
                    return memes
                
                return []
        except Exception as e:
            print(f"Error generating sample data: {e}")
            
            # Try to use actual files instead
            memes = find_meme_files(count)
            if memes:
                return memes
            
            return []
    
    # Convert DataFrame to list of dictionaries
    memes = df.to_dict(orient="records")
    
    # Add id for each meme
    for i, meme in enumerate(memes):
        meme["id"] = i
    
    # Limit to requested count
    memes = memes[:count]
    
    print(f"Returning {len(memes)} memes")
    return memes

@router.get("/real")
async def get_real_memes(count: int = Query(25, description="Number of memes to return")) -> List[Dict[str, Any]]:
    """Get a list of real memes directly from the image files in the dataset"""
    print(f"Received request for {count} real memes")
    
    # First try using the optimized function to find real meme files
    memes = find_meme_files(count)
    if memes:
        print(f"Returning {len(memes)} real memes from image files")
        return memes
    
    # If the optimized function doesn't find any memes, try a more direct approach
    print("Optimized function didn't find memes, trying direct file listing")
    
    if not os.path.exists(MEME_IMAGES_DIR):
        error_message = f"No meme images directory found at {MEME_IMAGES_DIR}"
        print(error_message)
        raise HTTPException(status_code=404, detail=error_message)
    
    try:
        # List the directory contents directly
        all_files = os.listdir(MEME_IMAGES_DIR)
        print(f"Found {len(all_files)} total files in directory")
        
        # Filter for image files
        image_files = [f for f in all_files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        print(f"Filtered to {len(image_files)} image files")
        
        if not image_files:
            error_message = "No image files found in dataset directory"
            print(error_message)
            raise HTTPException(status_code=404, detail=error_message)
        
        # Select random subset
        selected_files = random.sample(image_files, min(count, len(image_files)))
        print(f"Selected {len(selected_files)} random image files")
        
        # Create meme records
        result_memes = []
        for i, filename in enumerate(selected_files):
            result_memes.append({
                "id": i,
                "image_name": filename,
                "text": f"Meme {i+1}",
                "humour": random.choice(["not_funny", "funny", "very_funny"]),
                "sarcasm": random.choice(["not_sarcastic", "general", "twisted_meaning"]),
                "offensive": random.choice(["not_offensive", "slight", "very_offensive"]),
                "motivational": random.choice(["motivational", "not_motivational"]),
                "overall_sentiment": random.choice(["negative", "neutral", "positive"])
            })
        
        print(f"Returning {len(result_memes)} memes from direct directory listing")
        return result_memes
        
    except Exception as e:
        error_message = f"Error finding meme images: {str(e)}"
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)

@router.get("/random")
async def get_random_meme() -> Dict[str, Any]:
    """Get a random meme"""
    df = get_meme_data()
    
    if df.empty:
        # Try to find a random image from the dataset
        meme_files = find_meme_files(1)
        if meme_files:
            return meme_files[0]
        raise HTTPException(status_code=404, detail="No memes available")
    
    # Select a random meme
    random_meme = df.sample(1).iloc[0].to_dict()
    random_meme["id"] = random.randint(1, 1000)  # Add a random id
    
    return random_meme

@router.get("/{image_name}")
async def get_meme_image(image_name: str = Path(..., description="Name of the meme image file")):
    """Get a meme image by its filename"""
    print(f"Requested image: {image_name}")
    
    # Try different paths and extensions
    possible_paths = []
    
    # Check if the image exists in the sample directory
    sample_image_path = os.path.join(MEME_DIR, image_name)
    possible_paths.append(sample_image_path)
    
    # If it doesn't exist in the sample dir, check the original images directory
    # First try the exact name
    images_path = os.path.join(MEME_IMAGES_DIR, image_name)
    possible_paths.append(images_path)
    
    # Try different extensions
    base_name = os.path.splitext(image_name)[0]
    for ext in ['.jpg', '.jpeg', '.png', '.gif', '.JPG', '.JPEG', '.PNG', '.GIF']:
        image_path_with_ext = os.path.join(MEME_IMAGES_DIR, f"{base_name}{ext}")
        possible_paths.append(image_path_with_ext)
    
    # Also check for MemoryMatch_* images in the frontend public directory
    frontend_base = os.path.join("..", "frontend", "public", "memes")
    for ext in ['.jpg', '.jpeg', '.png', '.gif', '.JPG', '.JPEG', '.PNG', '.GIF']:
        frontend_path = os.path.join(frontend_base, f"{base_name}{ext}")
        possible_paths.append(frontend_path)
    
    # Try each path in order
    for path in possible_paths:
        if os.path.isfile(path):
            print(f"Found image at: {path}")
            return FileResponse(path)
    
    # Log the paths we tried
    print(f"Image not found. Tried paths: {possible_paths}")
    raise HTTPException(status_code=404, detail=f"Image {image_name} not found") 