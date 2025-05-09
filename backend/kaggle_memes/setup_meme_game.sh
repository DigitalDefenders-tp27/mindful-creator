#!/bin/bash

# Setup script for the Meme Memory Match game
# This script will:
# 1. Check for required dependencies
# 2. Create necessary directories
# 3. Download and prepare the dataset if needed
# 4. Start the API server

set -e  # Exit on error

echo "====== Meme Memory Match Game Setup ======"

# Get the backend directory (parent of this script's directory)
BACKEND_DIR="$(dirname "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)")"  # Get backend directory path
echo "Backend directory: $BACKEND_DIR"

# Check for required dependencies
echo "Checking dependencies..."

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed. Please install Python 3 and try again."
    exit 1
fi

# Check for pip
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is required but not installed. Please install pip3 and try again."
    exit 1
fi

# Check for Kaggle CLI
if ! python3 -c "import kaggle" &> /dev/null; then
    echo "Kaggle CLI not found. Installing..."
    pip3 install kaggle
fi

# Create Kaggle credentials directory if it doesn't exist
KAGGLE_DIR=~/.kaggle
if [ ! -d "$KAGGLE_DIR" ]; then
    echo "Creating Kaggle credentials directory..."
    mkdir -p "$KAGGLE_DIR"
fi

# Check for Kaggle credentials
KAGGLE_CREDS=~/.kaggle/kaggle.json
if [ ! -f "$KAGGLE_CREDS" ]; then
    echo "Kaggle credentials not found. You need to place your kaggle.json file in ~/.kaggle/"
    echo "You can download your Kaggle API credentials from https://www.kaggle.com/settings"
    echo "1. Go to 'Account' tab"
    echo "2. Click 'Create New API Token'"
    echo "3. Move the downloaded kaggle.json file to ~/.kaggle/"
    echo "4. Run: chmod 600 ~/.kaggle/kaggle.json"
    
    read -p "Do you want to continue setup without downloading the dataset? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    # Check permissions on kaggle.json
    PERMS=$(stat -c %a "$KAGGLE_CREDS" 2>/dev/null || stat -f %Lp "$KAGGLE_CREDS")
    if [ "$PERMS" != "600" ]; then
        echo "Setting correct permissions on Kaggle credentials..."
        chmod 600 "$KAGGLE_CREDS"
    fi
fi

# Install required Python packages
echo "Installing required Python packages..."
if [ -f "$BACKEND_DIR/requirements.txt" ]; then
    pip3 install -r "$BACKEND_DIR/requirements.txt"
else
    echo "Creating requirements.txt and installing packages..."
    cat > requirements.txt << EOL
pandas>=1.3.0
fastapi>=0.68.0
uvicorn>=0.15.0
kaggle>=1.5.12
python-multipart>=0.0.5
EOL
    pip3 install -r requirements.txt
fi

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p "$BACKEND_DIR/datasets/meme"

# Check if the dataset exists
DATASET_LABELS="$BACKEND_DIR/datasets/meme/memotion_dataset_7k/labels.csv"
SAMPLE_CSV="$BACKEND_DIR/datasets/meme/memotion_sample.csv"

if [ -f "$SAMPLE_CSV" ]; then
    echo "Sample dataset found. Skipping download and preparation."
elif [ -f "$DATASET_LABELS" ]; then
    echo "Dataset found. Preparing for use..."
    python3 meme_dataset_manager.py prepare
else
    if [ -f "$KAGGLE_CREDS" ]; then
        echo "Downloading and preparing dataset..."
        python3 meme_dataset_manager.py all --port 8001
        exit 0  # Exit as the 'all' command will also start the server
    else
        echo "Dataset not found and Kaggle credentials not available. Cannot proceed."
        echo "Please set up your Kaggle credentials and run this script again."
        exit 1
    fi
fi

# Start the API server
echo "Starting API server on port 8001..."
python3 meme_dataset_manager.py serve

echo "Setup complete!" 