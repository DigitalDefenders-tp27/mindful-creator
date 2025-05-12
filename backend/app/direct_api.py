from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import List, Dict, Any
import pandas as pd

app = FastAPI(
    title="Meme API",
    description="Direct API for serving meme images",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

@app.get("/")
async def root():
    return {"message": "Meme API is running"}

@app.get("/memes")
async def get_memes() -> List[Dict[str, Any]]:
    """Get a list of memes for the memory match game"""
    df = get_meme_data()
    
    if df.empty:
        return []
    
    # Convert DataFrame to list of dictionaries
    memes = df.to_dict(orient="records")
    
    # Add id for each meme
    for i, meme in enumerate(memes):
        meme["id"] = i
    
    return memes

@app.get("/memes/{image_name}")
async def get_meme_image(image_name: str):
    """Get a meme image by its filename"""
    # Check if the image exists in the sample directory
    sample_image_path = os.path.join(MEME_DIR, image_name)
    
    # If it doesn't exist in the sample dir, check the original images directory
    if not os.path.isfile(sample_image_path):
        sample_image_path = os.path.join(MEME_IMAGES_DIR, image_name)
    
    if not os.path.isfile(sample_image_path):
        raise HTTPException(status_code=404, detail=f"Image {image_name} not found")
    
    return FileResponse(sample_image_path) 