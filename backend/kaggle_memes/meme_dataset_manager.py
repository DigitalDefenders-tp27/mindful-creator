#!/usr/bin/env python3
"""
Meme Dataset Manager

This script provides functionality to download, prepare, and serve the
Memotion dataset for the memory match game.

Functions:
- download_dataset(): Downloads the dataset using Kaggle API
- prepare_dataset(): Prepares the dataset for the game
- serve_dataset(): Starts a FastAPI server to serve meme images

Usage:
    python meme_dataset_manager.py download
    python meme_dataset_manager.py prepare
    python meme_dataset_manager.py serve [--port PORT]
    python meme_dataset_manager.py all [--port PORT]
"""

import os
import sys
import argparse
import subprocess
import shutil
import random
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("meme_dataset_manager")

# Constants and paths
DATASET_ID = "williamscott701/memotion-dataset-7k"
# Use absolute path to ensure correct path regardless of where script is run from
DATASET_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "datasets", "meme")
IMAGES_DIR = os.path.join(DATASET_DIR, "memotion_dataset_7k", "images")
LABELS_CSV = os.path.join(DATASET_DIR, "memotion_dataset_7k", "labels.csv")
OUTPUT_DIR = DATASET_DIR
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "memotion_sample.csv")
DEFAULT_PORT = 8001

# FastAPI app for serving memes
app = FastAPI(
    title="Meme API",
    description="API for serving meme images",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def download_dataset() -> bool:
    """
    Download the Memotion dataset using the Kaggle API
    
    Returns:
        bool: True if download was successful, False otherwise
    """
    logger.info(f"Downloading dataset {DATASET_ID}...")
    
    # Ensure the dataset directory exists
    os.makedirs(DATASET_DIR, exist_ok=True)
    
    # Check if Kaggle credentials are available
    kaggle_cred_path = os.path.expanduser("~/.kaggle/kaggle.json")
    if not os.path.exists(kaggle_cred_path):
        logger.error(f"Kaggle credentials not found at {kaggle_cred_path}")
        logger.info("Make sure to place your kaggle.json file in ~/.kaggle/ with 600 permissions")
        return False
    
    try:
        # Run Kaggle CLI command to download the dataset
        cmd = ["kaggle", "datasets", "download", "-d", DATASET_ID, "-p", DATASET_DIR, "--unzip"]
        logger.info(f"Running command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info(result.stdout)
        
        if result.returncode == 0:
            logger.info("Dataset downloaded successfully")
            return True
        else:
            logger.error(f"Failed to download dataset: {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        logger.error(f"Error downloading dataset: {e}")
        if e.stdout:
            logger.info(f"STDOUT: {e.stdout}")
        if e.stderr:
            logger.error(f"STDERR: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error downloading dataset: {e}")
        return False

def check_dataset() -> bool:
    """
    Check if the dataset is available and update paths if needed
    
    Returns:
        bool: True if dataset is available, False otherwise
    """
    global IMAGES_DIR, LABELS_CSV
    
    if not os.path.exists(DATASET_DIR):
        logger.error(f"Dataset directory {DATASET_DIR} not found")
        return False
    
    if not os.path.exists(IMAGES_DIR):
        logger.warning(f"Images directory {IMAGES_DIR} not found")
        logger.info(f"Available files in {DATASET_DIR}:")
        for item in os.listdir(DATASET_DIR):
            logger.info(f"  - {item}")
        
        # Try to find the images directory
        if os.path.exists(os.path.join(DATASET_DIR, "images")):
            IMAGES_DIR = os.path.join(DATASET_DIR, "images")
            logger.info(f"Using images directory at {IMAGES_DIR} instead")
        else:
            return False
    
    if not os.path.exists(LABELS_CSV):
        logger.warning(f"Labels CSV {LABELS_CSV} not found")
        logger.info(f"Available files in {DATASET_DIR}:")
        for item in os.listdir(DATASET_DIR):
            logger.info(f"  - {item}")
            
        # Try to find any CSV file that might contain labels
        csv_files = [f for f in os.listdir(DATASET_DIR) if f.endswith('.csv')]
        if csv_files:
            LABELS_CSV = os.path.join(DATASET_DIR, csv_files[0])
            logger.info(f"Using {LABELS_CSV} instead")
        else:
            return False
    
    # Make sure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    return True

def copy_images(image_names: List[str], dest_dir: str) -> int:
    """
    Copy selected images to the destination directory
    
    Args:
        image_names: List of image filenames to copy
        dest_dir: Destination directory
        
    Returns:
        int: Number of successfully copied images
    """
    copied_count = 0
    for image_name in image_names:
        src_path = os.path.join(IMAGES_DIR, image_name)
        if os.path.exists(src_path):
            dest_path = os.path.join(dest_dir, image_name)
            try:
                shutil.copy2(src_path, dest_path)
                copied_count += 1
            except Exception as e:
                logger.error(f"Error copying {image_name}: {e}")
        else:
            logger.warning(f"Source image not found: {src_path}")
    
    return copied_count

def prepare_dataset() -> bool:
    """
    Prepare the dataset for the memory match game
    
    Returns:
        bool: True if preparation was successful, False otherwise
    """
    logger.info("Preparing dataset for the memory match game...")
    
    # First check if the dataset is available
    if not check_dataset():
        logger.error("Dataset check failed")
        return False
    
    try:
        # Load labels
        logger.info(f"Loading labels from {LABELS_CSV}")
        labels_df = pd.read_csv(LABELS_CSV)
        logger.info(f"Loaded {len(labels_df)} records")
        
        # Print columns to help with debugging
        logger.info(f"Dataset columns: {labels_df.columns.tolist()}")
        
        # Find image name column - it might have different names
        image_name_candidates = ['image_name', 'image', 'file_name', 'filename', 'img_name']
        image_name_col = None
        
        for col in image_name_candidates:
            if col in labels_df.columns:
                image_name_col = col
                break
        
        if not image_name_col:
            # Try to infer the column by looking for a column with image filenames
            for col in labels_df.columns:
                col_values = labels_df[col].astype(str)
                # Check if most values end with image extensions
                if col_values.str.endswith(('.jpg', '.jpeg', '.png', '.gif')).mean() > 0.5:
                    image_name_col = col
                    break
        
        if not image_name_col:
            logger.error(f"Could not identify image name column. Available columns: {labels_df.columns.tolist()}")
            # Use the first column as a fallback
            image_name_col = labels_df.columns[0]
            logger.warning(f"Using {image_name_col} as fallback for image names")
        
        logger.info(f"Using '{image_name_col}' as the image name column")
        
        # Create a sample of the dataset with a manageable number of images
        sample_size = min(25, len(labels_df))
        sample_df = labels_df.sample(sample_size, random_state=42)
        
        # Save sample dataset
        sample_df.to_csv(OUTPUT_CSV, index=False)
        logger.info(f"Saved {len(sample_df)} records to {OUTPUT_CSV}")
        
        # Copy the selected images
        image_names = sample_df[image_name_col].tolist()
        copied = copy_images(image_names, OUTPUT_DIR)
        logger.info(f"Copied {copied} images to {OUTPUT_DIR}")
        
        # Preview the sample dataset
        logger.info("\nSample dataset preview:")
        logger.info(sample_df.head(3).to_string())
        
        return True
    
    except Exception as e:
        logger.error(f"Error preparing dataset: {e}")
        import traceback
        traceback.print_exc()
        return False

def get_meme_data() -> pd.DataFrame:
    """
    Load meme data from the sample CSV file
    
    Returns:
        pd.DataFrame: DataFrame containing meme data
    """
    try:
        if os.path.exists(OUTPUT_CSV):
            logger.info(f"Loading meme data from {OUTPUT_CSV}")
            return pd.read_csv(OUTPUT_CSV)
        else:
            logger.warning(f"Sample CSV not found at {OUTPUT_CSV}")
            return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error loading meme data: {e}")
        return pd.DataFrame()

@app.get("/")
async def root():
    """API root endpoint"""
    return {"message": "Meme API is running"}

@app.get("/memes")
async def get_memes() -> List[Dict[str, Any]]:
    """Get a list of memes for the memory match game"""
    df = get_meme_data()
    
    if df.empty:
        logger.warning("No meme data found")
        return []
    
    # Convert DataFrame to list of dictionaries
    memes = df.to_dict(orient="records")
    
    # Add id for each meme
    for i, meme in enumerate(memes):
        meme["id"] = i
    
    logger.info(f"Returning {len(memes)} memes")
    return memes

@app.get("/memes/{image_name}")
async def get_meme_image(image_name: str):
    """Get a meme image by its filename"""
    logger.info(f"Request for image: {image_name}")
    
    # Check if the image exists in the sample directory
    sample_image_path = os.path.join(OUTPUT_DIR, image_name)
    logger.debug(f"Looking for image at: {sample_image_path}")
    
    # If it doesn't exist in the sample dir, check the original images directory
    if not os.path.isfile(sample_image_path):
        sample_image_path = os.path.join(IMAGES_DIR, image_name)
        logger.debug(f"Looking for image at: {sample_image_path}")
    
    if not os.path.isfile(sample_image_path):
        logger.warning(f"Image not found: {image_name}")
        raise HTTPException(status_code=404, detail=f"Image {image_name} not found")
    
    logger.info(f"Serving image from: {sample_image_path}")
    return FileResponse(sample_image_path)

def serve_dataset(port: int = DEFAULT_PORT) -> None:
    """
    Serve the meme dataset using FastAPI
    
    Args:
        port: Port number to run the server on
    """
    logger.info(f"Starting Meme API server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)

def main():
    """Main function to parse arguments and execute commands"""
    parser = argparse.ArgumentParser(description="Meme Dataset Manager")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Download command
    download_parser = subparsers.add_parser("download", help="Download the dataset")
    
    # Prepare command
    prepare_parser = subparsers.add_parser("prepare", help="Prepare the dataset")
    
    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Serve the dataset")
    serve_parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port to run the server on")
    
    # All-in-one command
    all_parser = subparsers.add_parser("all", help="Download, prepare, and serve the dataset")
    all_parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port to run the server on")
    
    args = parser.parse_args()
    
    if args.command == "download":
        download_dataset()
    elif args.command == "prepare":
        prepare_dataset()
    elif args.command == "serve":
        serve_dataset(args.port)
    elif args.command == "all":
        if download_dataset():
            if prepare_dataset():
                serve_dataset(args.port)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 