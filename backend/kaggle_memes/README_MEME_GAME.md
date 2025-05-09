# Meme Memory Match Game

This directory contains the backend code for the Meme Memory Match game, which uses the Memotion dataset from Kaggle.

## Overview

The Meme Memory Match game is a card-matching game that uses internet memes as card content. Players can learn about meme sentiment analysis, including humor, sarcasm, offensiveness, and motivational ratings for each meme.

## Setup

### Prerequisites

- Python 3.7 or higher
- Kaggle account and API credentials
- The following Python packages:
  - pandas
  - fastapi
  - uvicorn
  - kaggle

### Quick Setup

The easiest way to set up the game is to use the provided setup script:

```bash
# Make the script executable
chmod +x setup_meme_game.sh

# Run the setup script
./setup_meme_game.sh
```

This script will:
1. Check for required dependencies
2. Install needed Python packages
3. Set up Kaggle credentials (if not already done)
4. Download and prepare the dataset
5. Start the API server

### Manual Setup

If you prefer to set up manually:

1. Install required packages:
   ```bash
   pip install pandas fastapi uvicorn kaggle
   ```

2. Set up Kaggle credentials:
   - Download your Kaggle API token from https://www.kaggle.com/settings (Account tab -> Create New API Token)
   - Place the downloaded `kaggle.json` file in `~/.kaggle/`
   - Set appropriate permissions: `chmod 600 ~/.kaggle/kaggle.json`

3. Download and prepare the dataset:
   ```bash
   python meme_dataset_manager.py download
   python meme_dataset_manager.py prepare
   ```

4. Start the API server:
   ```bash
   python meme_dataset_manager.py serve
   ```

## Using the Meme Dataset Manager

The `meme_dataset_manager.py` script provides several commands:

- **Download dataset:**
  ```bash
  python meme_dataset_manager.py download
  ```

- **Prepare dataset for the game:**
  ```bash
  python meme_dataset_manager.py prepare
  ```

- **Start the API server:**
  ```bash
  python meme_dataset_manager.py serve [--port PORT]
  ```

- **Do all of the above:**
  ```bash
  python meme_dataset_manager.py all [--port PORT]
  ```

## API Endpoints

The meme API server provides the following endpoints:

- `GET /memes`: Returns a list of memes with their sentiment analysis
- `GET /memes/{image_name}`: Returns the image file for a specific meme

## Dataset Information

The Memotion dataset contains approximately 7,000 memes with sentiment analysis information, including:

- Humor rating (not_funny, funny, very_funny, hilarious)
- Sarcasm rating (not_sarcastic, general, twisted_meaning, very_twisted)
- Offensive rating (not_offensive, slight, very_offensive)
- Motivational rating (motivational, not_motivational)
- Overall sentiment (negative, neutral, positive, very_positive)

## Frontend Integration

The frontend component (`frontend/src/components/Games/MemoryMatch.vue`) connects to this API to display memes in the memory match game. It expects the API to be running on `http://localhost:8001`.

## Data Privacy and Storage

- The large dataset files (approximately 700MB) are excluded from version control via `.gitignore`.
- Only a small sample of memes (25 images) is prepared for the game.
- All data is stored locally on your machine.

## Troubleshooting

If you encounter issues:

1. **API server won't start**: Ensure no other service is using port 8001, or specify a different port.
2. **Dataset download fails**: Check your internet connection and Kaggle API credentials.
3. **Images not displaying**: Verify that the API server is running and check browser console for CORS errors.

## Credits

The Memotion dataset is from Kaggle: [Memotion Dataset 7K](https://www.kaggle.com/datasets/williamscott701/memotion-dataset-7k) 