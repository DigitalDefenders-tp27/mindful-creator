#!/usr/bin/env python3
"""
Copy Sample Memes to Frontend

This script copies a few sample meme images from the dataset to the frontend
public directory for display in the game selection UI.
"""

import os
import shutil
import random
from pathlib import Path

# Paths
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_IMAGES_DIR = os.path.join(BACKEND_DIR, "datasets", "meme", "memotion_dataset_7k", "images")
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
FRONTEND_PUBLIC_DIR = os.path.join(PROJECT_ROOT, "frontend", "public", "memes")

# Ensure the frontend memes directory exists
os.makedirs(FRONTEND_PUBLIC_DIR, exist_ok=True)

def main():
    """
    Main function to copy sample meme images to frontend
    """
    print("Copying sample meme images to frontend...")
    
    # Check if dataset images directory exists
    if not os.path.exists(DATASET_IMAGES_DIR):
        print(f"Error: Dataset images directory not found at {DATASET_IMAGES_DIR}")
        return False
    
    # Get a list of all image files
    all_image_files = [f for f in os.listdir(DATASET_IMAGES_DIR) 
                       if os.path.isfile(os.path.join(DATASET_IMAGES_DIR, f)) and 
                       f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    
    # Select 3 random images
    num_samples = min(3, len(all_image_files))
    if num_samples == 0:
        print("No image files found in the dataset directory.")
        return False
    
    sample_images = random.sample(all_image_files, num_samples)
    
    # Copy selected images to frontend public directory
    for idx, image_file in enumerate(sample_images):
        src_path = os.path.join(DATASET_IMAGES_DIR, image_file)
        dst_path = os.path.join(FRONTEND_PUBLIC_DIR, f"MemoryMatch_{idx + 1}.jpg")
        
        try:
            shutil.copy2(src_path, dst_path)
            print(f"Copied {image_file} to {dst_path}")
        except Exception as e:
            print(f"Error copying {image_file}: {e}")
    
    # Create a special main image
    main_image = sample_images[0] if sample_images else None
    if main_image:
        main_dst = os.path.join(FRONTEND_PUBLIC_DIR, "MemoryMatch.jpg")
        try:
            shutil.copy2(os.path.join(DATASET_IMAGES_DIR, main_image), main_dst)
            print(f"Copied main image to {main_dst}")
        except Exception as e:
            print(f"Error copying main image: {e}")
    
    print("Sample meme images copied successfully.")
    return True

if __name__ == "__main__":
    main() 