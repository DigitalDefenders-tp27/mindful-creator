#!/bin/bash

# Start the meme game
# This script:
# 1. Prepares sample meme images for the frontend
# 2. Starts the meme API server

set -e  # Exit on error

echo "====== Starting Meme Memory Match Game ======"

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Run the script to copy sample images to frontend
echo "Preparing sample images for frontend..."
python3 kaggle_memes/copy_frontend_samples.py

# Check if the dataset exists
if [ ! -d "./datasets/meme/memotion_dataset_7k" ]; then
    echo "Dataset not found. Please run setup script first:"
    echo "cd kaggle_memes && ./setup_meme_game.sh"
    exit 1
fi

# Start the API server
echo "Starting meme API server..."
echo "Press Ctrl+C to stop the server when done."
python3 kaggle_memes/meme_dataset_manager.py serve 