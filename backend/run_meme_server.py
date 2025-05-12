#!/usr/bin/env python3
"""
Run a standalone FastAPI server for the Memory Match game.

This script:
1. Checks for the meme dataset
2. Starts a FastAPI server to serve meme data and images
"""

import os
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import importlib.util
import subprocess

# Paths
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BACKEND_DIR, "datasets", "meme")
DATASET_IMAGES_DIR = os.path.join(DATASET_DIR, "memotion_dataset_7k", "images")
SAMPLE_CSV = os.path.join(DATASET_DIR, "memotion_sample.csv")

def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = ["fastapi", "uvicorn", "pandas"]
    
    for package in required_packages:
        try:
            importlib.util.find_spec(package)
        except ImportError:
            print(f"Required package '{package}' is not installed.")
            print(f"Please install it with: pip install {package}")
            return False
    
    return True

def check_dataset():
    """Check if the meme dataset exists and is properly set up"""
    if not os.path.exists(DATASET_DIR):
        print(f"Error: Dataset directory not found at {DATASET_DIR}")
        print("Please download the dataset first using the setup_meme_game.sh script")
        return False
    
    if not os.path.exists(DATASET_IMAGES_DIR):
        print(f"Error: Meme images directory not found at {DATASET_IMAGES_DIR}")
        print("Please download the dataset first using the setup_meme_game.sh script")
        return False
    
    # Check if there are any images in the directory
    image_count = len([f for f in os.listdir(DATASET_IMAGES_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    if image_count == 0:
        print(f"Error: No image files found in {DATASET_IMAGES_DIR}")
        print("Please download the dataset first using the setup_meme_game.sh script")
        return False
    
    print(f"Found {image_count} meme images in the dataset")
    
    # Check for sample CSV
    if not os.path.exists(SAMPLE_CSV):
        print(f"Warning: Sample CSV not found at {SAMPLE_CSV}")
        print("Will attempt to generate sample dataset from full dataset")
    else:
        print(f"Found sample CSV with meme data")
    
    return True

def create_sample_dataset():
    """Create a sample dataset if it doesn't exist"""
    if os.path.exists(SAMPLE_CSV):
        print(f"Sample dataset already exists at {SAMPLE_CSV}")
        return True
    
    try:
        # Run the prepare_memes_for_game.py script
        prepare_script = os.path.join(BACKEND_DIR, "prepare_memes_for_game.py")
        if os.path.exists(prepare_script):
            print("Running prepare_memes_for_game.py to create sample dataset...")
            subprocess.run(["python3", prepare_script], check=True)
            if os.path.exists(SAMPLE_CSV):
                print(f"Successfully created sample dataset at {SAMPLE_CSV}")
                return True
            else:
                print(f"Failed to create sample dataset")
        else:
            print(f"Warning: prepare_memes_for_game.py script not found at {prepare_script}")
    except Exception as e:
        print(f"Error creating sample dataset: {e}")
    
    return False

def copy_frontend_samples():
    """Copy sample memes to frontend public directory"""
    try:
        copy_script = os.path.join(BACKEND_DIR, "copy_sample_memes.py")
        if os.path.exists(copy_script):
            print("Copying sample meme images to frontend directory...")
            subprocess.run(["python3", copy_script], check=True)
            print("Sample images copied to frontend")
        else:
            print(f"Warning: copy_sample_memes.py script not found at {copy_script}")
    except Exception as e:
        print(f"Error copying frontend samples: {e}")

def run_server():
    """Run the FastAPI server for meme game"""
    print("Starting FastAPI server for Memory Match game...")
    
    sys.path.insert(0, BACKEND_DIR)
    os.chdir(BACKEND_DIR)
    
    # Import app.main dynamically
    try:
        from app.main import app
        
        # Mount the meme images directory as static files
        print(f"Mounting meme images directory: {DATASET_IMAGES_DIR}")
        if os.path.exists(DATASET_IMAGES_DIR):
            app.mount("/meme-images", StaticFiles(directory=DATASET_IMAGES_DIR), name="meme-images")
            print(f"Successfully mounted {DATASET_IMAGES_DIR} at /meme-images")
        else:
            print(f"Warning: Images directory not found at {DATASET_IMAGES_DIR}")
        
        # Also mount the frontend/public/memes directory if it exists
        frontend_memes_dir = os.path.join(BACKEND_DIR, "..", "frontend", "public", "memes")
        if os.path.exists(frontend_memes_dir):
            app.mount("/frontend-memes", StaticFiles(directory=frontend_memes_dir), name="frontend-memes")
            print(f"Successfully mounted {frontend_memes_dir} at /frontend-memes")
        
        # Run the server
        print("Starting server on http://localhost:8001")
        uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
    except ImportError as e:
        print(f"Failed to import app.main: {e}")
        print("Using standalone app instead")
        
        # Create a standalone app if app.main cannot be imported
        from app.routers.memes import router as memes_router
        
        app = FastAPI(title="Memory Match Game API")
        
        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Include memes router
        app.include_router(memes_router, prefix="/api/memes")
        
        # Mount the meme images directory as static files
        print(f"Mounting meme images directory: {DATASET_IMAGES_DIR}")
        if os.path.exists(DATASET_IMAGES_DIR):
            app.mount("/meme-images", StaticFiles(directory=DATASET_IMAGES_DIR), name="meme-images")
            print(f"Successfully mounted {DATASET_IMAGES_DIR} at /meme-images")
        else:
            print(f"Warning: Images directory not found at {DATASET_IMAGES_DIR}")
        
        # Also mount the frontend/public/memes directory if it exists
        frontend_memes_dir = os.path.join(BACKEND_DIR, "..", "frontend", "public", "memes")
        if os.path.exists(frontend_memes_dir):
            app.mount("/frontend-memes", StaticFiles(directory=frontend_memes_dir), name="frontend-memes")
            print(f"Successfully mounted {frontend_memes_dir} at /frontend-memes")
        
        # Root endpoint
        @app.get("/")
        async def root():
            return {"message": "Memory Match Game API is running"}
        
        # Run the server
        print("Starting server on http://localhost:8001")
        uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")

if __name__ == "__main__":
    print("=" * 50)
    print("MEMORY MATCH GAME BACKEND SERVER")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check for dataset
    if not check_dataset():
        sys.exit(1)
    
    # Create sample dataset if needed
    create_sample_dataset()
    
    # Copy sample images to frontend
    copy_frontend_samples()
    
    # Run the server
    run_server() 