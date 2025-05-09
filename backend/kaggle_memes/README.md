# Kaggle Meme Dataset Manager

Simple toolset for working with the Memotion meme dataset from Kaggle.

## Quick Start

To download, prepare and serve the meme dataset in one command:

```bash
# Make the script executable
chmod +x setup_meme_game.sh

# Run the setup script
./setup_meme_game.sh
```

## Manual Usage

### Prerequisites

- Python 3.7 or higher
- Kaggle API credentials (see below)
- Required packages: pandas, fastapi, uvicorn, kaggle

### Kaggle API Setup

1. Sign up for a Kaggle account at https://www.kaggle.com
2. Go to your account settings (click on your profile picture → Account)
3. Scroll down to API section and click "Create New API Token"
4. Move the downloaded `kaggle.json` file to `~/.kaggle/`
5. Set permissions: `chmod 600 ~/.kaggle/kaggle.json`

### Using the Script

The `meme_dataset_manager.py` script has several commands:

```bash
# Download the dataset
python3 meme_dataset_manager.py download

# Prepare the dataset for use (create a sample)
python3 meme_dataset_manager.py prepare

# Serve the dataset via API
python3 meme_dataset_manager.py serve

# Or do everything in one command
python3 meme_dataset_manager.py all
```

## Dataset

The script will download the [Memotion Dataset 7K](https://www.kaggle.com/datasets/williamscott701/memotion-dataset-7k) from Kaggle.

## API

When running the API server, it will be available at:
- Base URL: http://localhost:8001
- Endpoints:
  - GET /memes - List all memes
  - GET /memes/{image_name} - Get a specific meme image

## For More Information

See [README_MEME_GAME.md](README_MEME_GAME.md) for more detailed documentation. 