# Backend Organization

This document explains the organization of the backend directory, focusing on the Kaggle-related files and meme game components.

## Directory Structure

The backend structure has been reorganized for better maintainability:

```
backend/
├── app/                  # Main FastAPI application
├── datasets/             # Dataset storage (not committed to git)
│   └── meme/             # Meme dataset files
├── kaggle_memes/         # Kaggle meme game code
│   ├── meme_dataset_manager.py   # Main script for dataset management
│   ├── setup_meme_game.sh        # Setup script for the game
│   ├── organize_meme_files.py    # Script that organized these files
│   ├── README_MEME_GAME.md       # Detailed documentation for the meme game
│   └── ...                       # Other meme-related utility scripts
├── meme_game.py          # Symbolic link to kaggle_memes/meme_dataset_manager.py
└── ...                   # Other backend files
```

## Using the Meme Game

### Quick Setup

To set up and run the meme game:

```bash
# From the backend directory
cd kaggle_memes
./setup_meme_game.sh
```

Or use the symbolic link from the backend directory:

```bash
# From the backend directory
python3 meme_game.py all
```

### Running Specific Commands

The meme game supports several commands:

```bash
# Download the dataset
python3 meme_game.py download

# Prepare the dataset for the game
python3 meme_game.py prepare

# Start the API server
python3 meme_game.py serve

# Download, prepare, and serve in one command
python3 meme_game.py all
```

## Dataset Storage

The Memotion dataset is stored in the `backend/datasets/meme/` directory but is not committed to git due to its size. The `.gitignore` file is configured to exclude these large files.

## Frontend Integration

The frontend component (`frontend/src/components/Games/MemoryMatch.vue`) connects to the meme API which serves images and metadata. The API runs on port 8001 by default.

## Documentation

For detailed documentation on the meme game, please refer to `backend/kaggle_memes/README_MEME_GAME.md`.

## Maintenance

To make changes to the meme game, modify the files in the `kaggle_memes` directory. The symbolic link `meme_game.py` will always point to the latest version. 