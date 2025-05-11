from fastapi import APIRouter, Depends, HTTPException, Query
import pandas as pd
import random
import os
import glob
from typing import List, Dict, Optional, Any
import shutil
import httpx
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
# Try to build from Railway-specific environment variables first for internal connections
PGHOST = os.getenv("PGHOST")
PGUSER = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD")
PGDATABASE = os.getenv("PGDATABASE")
PGPORT = os.getenv("PGPORT", "5432") # Default PostgreSQL port

# Prioritize DATABASE_URL_MEME_FETCH if explicitly set by the user
DATABASE_URL_OVERRIDE = os.getenv("DATABASE_URL_MEME_FETCH")

if DATABASE_URL_OVERRIDE:
    DATABASE_URL = DATABASE_URL_OVERRIDE
    logger.info(f"Using explicit DATABASE_URL_MEME_FETCH: {DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else 'ตรวจสอบการตั้งค่า DATABASE_URL'}")
elif PGHOST and PGUSER and PGPASSWORD and PGDATABASE:
    # If PGHOST is provided, use it. Otherwise, default to postgres.railway.internal if other PG vars are set.
    db_host = PGHOST if PGHOST == "postgres.railway.internal" or "." in PGHOST else "postgres.railway.internal" # ensure it's either internal or a FQDN
    DATABASE_URL = f"postgresql://{PGUSER}:{PGPASSWORD}@{db_host}:{PGPORT}/{PGDATABASE}"
    logger.info(f"Constructed DATABASE_URL from PG* env vars for Railway: {DATABASE_URL.split('@')[-1]}")
else:
    DATABASE_URL = None # No valid configuration found
    logger.error("DATABASE_URL_MEME_FETCH is not set, and insufficient PG* environment variables found for Railway internal connection.")
    logger.info("Please set DATABASE_URL_MEME_FETCH or ensure PGHOST, PGUSER, PGPASSWORD, PGDATABASE are set for internal Railway connections.")

# Path constants for the new mechanism
FRONTEND_PUBLIC_DIR = Path("frontend/public")
TEMP_MEMES_SUBDIR = "temp_memes" # This will be inside frontend/public/
ABSOLUTE_TEMP_MEMES_DIR = FRONTEND_PUBLIC_DIR / TEMP_MEMES_SUBDIR

# Path to the meme dataset
MEME_DATASET_PATH = "backend/datasets/meme"
# Path to public meme directory
PUBLIC_MEME_PATH = "frontend/public/memes"

# Pydantic models for new endpoints
class GameInitRequest(BaseModel):
    level: int

class MemeData(BaseModel):
    id: Any 
    image_name: str
    imagePath: str 
    text: str
    humour: str | None
    sarcasm: str | None
    offensive: str | None
    motivational: str | None
    overall_sentiment: str | None

# Helper functions for the new mechanism
async def get_db_connection():
    if not DATABASE_URL:
        logger.error("Cannot connect to DB: DATABASE_URL_MEME_FETCH is not set.")
        raise HTTPException(status_code=500, detail="Database configuration error.")
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        logger.info(f"Successfully connected to database via {DATABASE_URL.split('@')[-1] if DATABASE_URL and '@' in DATABASE_URL else 'DATABASE_URL'}")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to database ({DATABASE_URL.split('@')[-1] if DATABASE_URL and '@' in DATABASE_URL else 'DATABASE_URL'}): {e}")
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

def ensure_temp_dir_exists_and_is_empty():
    """Ensures the temporary meme directory exists and is empty."""
    try:
        if ABSOLUTE_TEMP_MEMES_DIR.exists():
            for item in ABSOLUTE_TEMP_MEMES_DIR.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
        else:
            ABSOLUTE_TEMP_MEMES_DIR.mkdir(parents=True, exist_ok=True)
        logger.info(f"Temporary directory {ABSOLUTE_TEMP_MEMES_DIR} ensured and emptied.")
    except Exception as e:
        logger.error(f"Error managing temporary directory {ABSOLUTE_TEMP_MEMES_DIR}: {e}")
        raise HTTPException(status_code=500, detail=f"Could not initialize temporary storage: {e}")

# New Endpoints using PostgreSQL
@router.post("/memory_match/initialize_game", response_model=List[MemeData])
async def initialize_game_data_from_db(request: GameInitRequest):
    level = request.level
    if level == 1:
        num_memes_to_fetch = 6
    elif level == 2:
        num_memes_to_fetch = 25
    else:
        raise HTTPException(status_code=400, detail="Invalid game level specified. Must be 1 or 2.")

    ensure_temp_dir_exists_and_is_empty()
    
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
            logger.warning(f"Could only retrieve {len(db_records)}/{num_memes_to_fetch} memes from DB for level {level}.")
            if not db_records: # If no records at all
                 raise HTTPException(status_code=404, detail="Not enough memes found in the database to start the game.")
        
        processed_memes_data: List[MemeData] = []
        meme_id_counter = 1 

        async with httpx.AsyncClient(timeout=15.0) as client: # Increased timeout for downloads
            for record_idx, record in enumerate(db_records):
                image_name_from_db = record["image_name"]
                image_url = record["image_url"]
                
                if not image_name_from_db or not image_url:
                    logger.warning(f"Skipping record (idx: {record_idx}) due to missing image_name or image_url: {record}")
                    continue

                local_filename = Path(image_name_from_db).name 
                local_image_path_absolute = ABSOLUTE_TEMP_MEMES_DIR / local_filename
                
                try:
                    logger.info(f"Downloading: {image_url} to {local_image_path_absolute}")
                    response = await client.get(image_url)
                    
                    if response.status_code == 404:
                        logger.warning(f"Image not found (404) at URL: {image_url}. Skipping this meme.")
                        continue
                    response.raise_for_status() 
                    
                    with open(local_image_path_absolute, "wb") as f:
                        f.write(response.content)
                    logger.info(f"Saved: {local_filename}")
                    
                    frontend_accessible_path = f"/{TEMP_MEMES_SUBDIR}/{local_filename}"
                    
                    processed_memes_data.append(MemeData(
                        id=meme_id_counter,
                        image_name=local_filename,
                        imagePath=frontend_accessible_path,
                        text=str(record["text_corrected"] or f"Meme {meme_id_counter}"),
                        humour=record["humour"],
                        sarcasm=record["sarcasm"],
                        offensive=record["offensive"],
                        motivational=record["motivational"],
                        overall_sentiment=record["overall_sentiment"]
                    ))
                    meme_id_counter += 1
                    
                except httpx.HTTPStatusError as e:
                    logger.error(f"HTTP error {e.response.status_code} for {image_url}: {e}")
                except httpx.RequestError as e: # Covers network errors, timeouts, etc.
                    logger.error(f"Request error for {image_url}: {e}")
                except Exception as e: # Catch any other unexpected errors during download/processing
                    logger.error(f"Unexpected error processing image {image_url} (Name: {image_name_from_db}): {e}")
                
                if len(processed_memes_data) >= num_memes_to_fetch: # Should match the outer loop logic but good for safety
                    break
        
        if len(processed_memes_data) < num_memes_to_fetch:
            logger.warning(f"Successfully prepared {len(processed_memes_data)} memes, but expected {num_memes_to_fetch}.")
            if not processed_memes_data: # If still no memes after trying to download
                 raise HTTPException(status_code=500, detail="Failed to download and prepare any memes for the game.")
        
        logger.info(f"Returning {len(processed_memes_data)} memes for level {level}.")
        return processed_memes_data
        
    except asyncpg.PostgresError as e:
        logger.error(f"Database query error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except HTTPException: 
        raise
    except Exception as e:
        logger.error(f"Unexpected error in initialize_game_data_from_db: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected server error occurred: {e}")
    finally:
        if conn and not conn.is_closed():
            await conn.close()
            logger.info("Database connection closed.")

@router.post("/memory_match/cleanup_game")
async def cleanup_temporary_memes_endpoint(): # Renamed function slightly for clarity
    try:
        if ABSOLUTE_TEMP_MEMES_DIR.exists():
            shutil.rmtree(ABSOLUTE_TEMP_MEMES_DIR) # Remove the entire directory
            ABSOLUTE_TEMP_MEMES_DIR.mkdir(parents=True, exist_ok=True) # Recreate for next session
            logger.info(f"Cleaned up and recreated temporary memes directory: {ABSOLUTE_TEMP_MEMES_DIR}")
        else:
            logger.info(f"Temporary memes directory {ABSOLUTE_TEMP_MEMES_DIR} not found, creating it.")
            ABSOLUTE_TEMP_MEMES_DIR.mkdir(parents=True, exist_ok=True)
        return {"message": "Temporary memes storage managed successfully."}
    except Exception as e:
        logger.error(f"Error managing temporary memes directory {ABSOLUTE_TEMP_MEMES_DIR}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to manage temporary memes storage: {e}")

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