from fastapi import APIRouter, Depends, HTTPException, Query
import pandas as pd
import random
import os
import glob
from typing import List, Dict, Optional, Any
import asyncpg
from pathlib import Path
import logging
from pydantic import BaseModel

router = APIRouter()

# Setup logger
logger = logging.getLogger(__name__)
# Configure logging if not already done globally, e.g.:
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Database Configuration
PGHOST_ENV = os.getenv("PGHOST")
PGUSER_ENV = os.getenv("PGUSER")
PGPASSWORD_ENV = os.getenv("PGPASSWORD")
PGDATABASE_ENV = os.getenv("PGDATABASE")
PGPORT_ENV = os.getenv("PGPORT", "5432") # Default PostgreSQL port

# Diagnostic logging for environment variables
logger.info(f"Read PGHOST_ENV: '{PGHOST_ENV}' (Type: {type(PGHOST_ENV)})")
logger.info(f"Read PGUSER_ENV: '{PGUSER_ENV}' (Type: {type(PGUSER_ENV)})")
logger.info(f"Read PGPASSWORD_ENV: '{'********' if PGPASSWORD_ENV else PGPASSWORD_ENV}' (Type: {type(PGPASSWORD_ENV)})") # Mask password
logger.info(f"Read PGDATABASE_ENV: '{PGDATABASE_ENV}' (Type: {type(PGDATABASE_ENV)})")
logger.info(f"Read PGPORT_ENV: '{PGPORT_ENV}' (Type: {type(PGPORT_ENV)})")

# Logic for DATABASE_URL_MEME_FETCH override has been removed.
# The application will now solely rely on PG* environment variables.

if PGHOST_ENV and PGUSER_ENV and PGPASSWORD_ENV and PGDATABASE_ENV:
    # Ensure db_host is correctly determined for Railway internal or external hostnames
    db_host = PGHOST_ENV
    # A simple check for internal might be if it doesn't contain '.', but Railway's PGHOST might be a FQDN.
    # The original logic: db_host = PGHOST if PGHOST == "postgres.railway.internal" or "." in PGHOST else "postgres.railway.internal"
    # This simplifies to just using PGHOST as provided by Railway, which should be the correct resolvable hostname.
    DATABASE_URL = f"postgresql://{PGUSER_ENV}:{PGPASSWORD_ENV}@{db_host}:{PGPORT_ENV}/{PGDATABASE_ENV}"
    logger.info(f"Constructed DATABASE_URL from PG* env vars. Connecting to host: {db_host}")
else:
    DATABASE_URL = None # No valid configuration found
    logger.error("Insufficient PG* environment variables (PGHOST, PGUSER, PGPASSWORD, PGDATABASE) found to construct DATABASE_URL.")
    logger.info("Ensure these environment variables are correctly set and injected by your hosting provider (e.g., Railway).")

# Path constants for the new mechanism
# FRONTEND_PUBLIC_DIR = Path("frontend/public")
# TEMP_MEMES_SUBDIR = "temp_memes" # This will be inside frontend/public/
# ABSOLUTE_TEMP_MEMES_DIR = FRONTEND_PUBLIC_DIR / TEMP_MEMES_SUBDIR

# Path to the meme dataset
MEME_DATASET_PATH = "backend/datasets/meme"
# Path to public meme directory
PUBLIC_MEME_PATH = "frontend/public/memes"

# Pydantic models for new endpoints
class GameInitRequest(BaseModel):
    level: int

class MemeDataFromDB(BaseModel): # Renamed to distinguish from frontend's potential MemeData
    id: Any 
    image_name: str # Keep for reference if needed
    image_url: str # This will be the original URL from the DB
    text: str
    humour: str | None
    sarcasm: str | None
    offensive: str | None
    motivational: str | None
    overall_sentiment: str | None

# Helper functions for the new mechanism
async def get_db_connection():
    if not DATABASE_URL:
        logger.error("Cannot connect to DB: DATABASE_URL is not configured.")
        raise HTTPException(status_code=500, detail="Database configuration error.")
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        logger.info(f"DB Connected: {DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else 'DB'}")
        return conn
    except Exception as e:
        logger.error(f"DB Connection Failed: {e}")
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

# New Endpoints using PostgreSQL
@router.post("/initialize_game", response_model=List[MemeDataFromDB])
async def initialize_game_data_from_db(request: GameInitRequest):
    level = request.level
    num_memes_to_fetch = 30 # User requested 30 memes; clarify if this is for game pairs or a general pool
                           # For Memory Match, we usually need N pairs. If it's 30 total unique images, frontend makes 15 pairs.
                           # Or, if it means 30 *pairs*, then 30 unique images. Or if it's just a data table for other use, then 30 is fine.
                           # Sticking to game pairs logic: Level 1 = 6 unique memes, Level 2 = 25 unique memes.
    if level == 1:
        num_memes_to_fetch = 6
    elif level == 2:
        num_memes_to_fetch = 25
    else:
        # If user wants a fixed 30 for a "table" regardless of level, adjust this logic.
        # For now, assuming level dictates pair count for the game.
        raise HTTPException(status_code=400, detail="Invalid game level specified. Must be 1 or 2 for standard game setup.")

    conn = None
    try:
        conn = await get_db_connection()
        query = """
            SELECT image_name, image_url, text_corrected, humour, sarcasm, offensive, motivational, overall_sentiment
            FROM meme_fetch
            WHERE image_url IS NOT NULL AND image_url <> '' AND image_name IS NOT NULL AND image_name <> ''
            ORDER BY RANDOM()
            LIMIT $1
        """
        db_records = await conn.fetch(query, num_memes_to_fetch)
        
        if not db_records or len(db_records) < num_memes_to_fetch:
            logger.warning(f"DB: Retrieved {len(db_records)}/{num_memes_to_fetch} memes for level {level}.")
            if not db_records:
                 raise HTTPException(status_code=404, detail="Not enough memes in DB for game.")
        
        processed_memes_data: List[MemeDataFromDB] = []
        meme_id_counter = 1 # Simple sequential ID for this batch

        for record in db_records:
            image_name_from_db = record["image_name"]
            image_url_from_db = record["image_url"]
            
            if not image_url_from_db: # Should be caught by WHERE clause, but good to check
                logger.warning(f"Skipping record with missing image_url: {image_name_from_db}")
                continue
            
            processed_memes_data.append(MemeDataFromDB(
                id=meme_id_counter, # This ID is just for this batch
                image_name=image_name_from_db,
                image_url=image_url_from_db, # Return the original URL
                text=str(record["text_corrected"] or f"Meme {meme_id_counter}"),
                humour=record["humour"],
                sarcasm=record["sarcasm"],
                offensive=record["offensive"],
                motivational=record["motivational"],
                overall_sentiment=record["overall_sentiment"]
            ))
            meme_id_counter += 1
        
        logger.info(f"Returning {len(processed_memes_data)} meme data objects (with URLs) for level {level}.")
        return processed_memes_data
        
    except asyncpg.PostgresError as e:
        logger.error(f"DB query error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in initialize_game_data_from_db: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected server error: {e}")
    finally:
        if conn and not conn.is_closed():
            await conn.close()
            logger.info("DB connection closed.")

# The cleanup_temporary_memes_endpoint is no longer needed as frontend handles its own temp storage (Object URLs)
# @router.post("/memory_match/cleanup_game")
# async def cleanup_temporary_memes_endpoint(): ...

def ensure_meme_directory_exists():
    """Ensure that the meme directory exists."""
    if not os.path.exists(MEME_DATASET_PATH):
        os.makedirs(MEME_DATASET_PATH, exist_ok=True)
        # Create a README file to explain the directory purpose
        with open(os.path.join(MEME_DATASET_PATH, "README.md"), "w") as f:
            f.write("# Meme Dataset Directory\n\nThis directory contains meme images from the Memotion dataset for the memory match game.")

def get_meme_data() -> pd.DataFrame:
    """
    Load the meme dataset from a CSV file.
    Falls back to the sample dataset if the full dataset is not available.
    """
    logger.info("get_meme_data() called - this may be deprecated by the new DB approach.")
    # Ensure directory exists
    ensure_meme_directory_exists()
    
    # Try to load the full dataset
    full_dataset_path = os.path.join(MEME_DATASET_PATH, "memotion_dataset.csv")
    
    # Check for sample dataset if full dataset doesn't exist
    sample_dataset_path = "backend/datasets/memotion_sample.csv"
    
    # Load the dataset
    if os.path.exists(full_dataset_path):
        try:
            return pd.read_csv(full_dataset_path)
        except Exception as e:
            print(f"Error loading full dataset: {e}")
    
    # Try sample dataset as fallback
    if os.path.exists(sample_dataset_path):
        try:
            return pd.read_csv(sample_dataset_path)
        except Exception as e:
            print(f"Error loading sample dataset: {e}")
            
    # If both fail, return an empty DataFrame with the expected columns
    return pd.DataFrame({
        'image_name': [], 
        'text_corrected': [], 
        'overall_sentiment': [],
        'humour': [],
        'sarcasm': [],
        'offensive': [],
        'motivational': []
    })

@router.get("/memory-match")
async def get_memes_for_memory_match(
    level: int = Query(1, description="Game level: 1 (6 pairs) or 2 (25 pairs) - DEPRECATED")
) -> Dict:
    """
    DEPRECATED: Get random memes for the memory match game from CSV.
    Use POST /api/games/memory_match/initialize_game instead.
    
    Args:
        level: Game level (1 or 2)
    
    Returns:
        Dict containing meme information for the game
    """
    logger.warning("Deprecated endpoint /memory-match called. Use POST /api/games/memory_match/initialize_game.")
    # Validate level
    if level not in [1, 2]:
        raise HTTPException(status_code=400, detail="Level must be 1 or 2")
    
    # Number of unique memes to fetch (level 1: 6 memes, level 2: 25 memes) - updated counts
    num_memes = 6 if level == 1 else 25
    
    # Load the dataset
    df = get_meme_data()
    
    # Check if the dataset is empty
    if df.empty:
        raise HTTPException(status_code=404, detail="Meme dataset (CSV) not found or empty")
    
    # Ensure we have required columns
    required_columns = ['image_name', 'text_corrected', 'overall_sentiment']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise HTTPException(
            status_code=500, 
            detail=f"Dataset (CSV) is missing required columns: {missing_columns}"
        )
    
    # Randomly select memes
    selected_memes_output = [] # Renamed to avoid conflict with MemeData model
    
    # If dataset has fewer rows than required, use them all
    if len(df) < num_memes: # Adjusted to check for less than, not less than or equal
        selected_indices = list(range(len(df)))
        logger.warning(f"Dataset (CSV) has only {len(df)} memes, requested {num_memes}. Using all available.")
    else:
        selected_indices = random.sample(range(len(df)), num_memes)
    
    for idx_val in selected_indices: # Renamed idx to idx_val to avoid conflict
        row = df.iloc[idx_val]
        
        sentiment_data = {
            'overall': row.get('overall_sentiment', 'neutral'),
            'humour': row.get('humour', 'unknown'),
            'sarcasm': row.get('sarcasm', 'unknown'),
            'offensive': row.get('offensive', 'unknown'),
            'motivational': row.get('motivational', 'unknown')
        }
        
        meme_item = { # Renamed to avoid conflict
            'id': int(idx_val), 
            'image_name': row['image_name'],
            'text': row.get('text_corrected', ''),
            'sentiment': sentiment_data,
            'imagePath': f"/memes/{row['image_name']}" if 'image_name' in row and row['image_name'] else None
        }
        selected_memes_output.append(meme_item)
    
    return {
        "level": level,
        "memes": selected_memes_output,
        "message": "This endpoint is deprecated. Use POST /api/games/memory_match/initialize_game."
    }

@router.get("/scan-memes")
async def scan_available_memes() -> List[str]:
    """
    Scan for available meme images in the public directory and test_memes.
    (This function's relevance might change with the new DB-focused approach)
    """
    logger.info("scan_available_memes() called - its relevance may change.")
    all_meme_paths = []
    
    # Check the main public meme directory
    if os.path.exists(PUBLIC_MEME_PATH):
        for ext in ['jpg', 'jpeg', 'png', 'gif']:
            pattern = os.path.join(PUBLIC_MEME_PATH, f"*.{ext}")
            all_meme_paths.extend(glob.glob(pattern))
    
    # Always include the fallback test meme directory if we're in development
    test_meme_paths = []
    test_dir = "backend/datasets/test_memes" # This path seems specific to a dev setup
    if os.path.exists(test_dir):
        for ext in ['jpg', 'jpeg', 'png', 'gif']:
            pattern = os.path.join(test_dir, f"*.{ext}")
            test_meme_paths.extend(glob.glob(pattern))
    
    public_meme_files = [os.path.basename(p) for p in all_meme_paths]
    test_meme_files = [os.path.basename(p) for p in test_meme_paths]
    
    all_meme_files = list(set(public_meme_files + test_meme_files))
    
    logger.info(f"Found {len(all_meme_files)} unique meme files across {PUBLIC_MEME_PATH} and {test_dir}")
    
    return all_meme_files 