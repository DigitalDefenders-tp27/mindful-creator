from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import FileResponse
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

# Path constants for the new mechanism
# FRONTEND_PUBLIC_DIR = Path("frontend/public")
# TEMP_MEMES_SUBDIR = "temp_memes" # This will be inside frontend/public/
# ABSOLUTE_TEMP_MEMES_DIR = FRONTEND_PUBLIC_DIR / TEMP_MEMES_SUBDIR

# Path to the meme dataset
MEME_DATASET_PATH = "backend/datasets/meme"
# Path to public meme directory
PUBLIC_MEME_PATH = "frontend/public/memes"

# This path should correspond to where images were downloaded in your Dockerfile
MEME_IMAGE_DIR = Path("/app/meme_images") 

# Pydantic models for new endpoints
class GameInitRequest(BaseModel):
    level: int

# Renamed Pydantic model for clarity
class MemeDataWithLocalURL(BaseModel):
    id: Any 
    image_name: str 
    image_url: str # This will now be a URL to our backend's serving endpoint
    text: str
    humour: Optional[str] = None
    sarcasm: Optional[str] = None
    offensive: Optional[str] = None
    motivational: Optional[str] = None
    overall_sentiment: Optional[str] = None

# Helper functions for the new mechanism
async def get_db_connection():
    PGHOST_ENV = os.getenv("PGHOST")
    PGUSER_ENV = os.getenv("PGUSER")
    PGPASSWORD_ENV = os.getenv("PGPASSWORD")
    PGDATABASE_ENV = os.getenv("PGDATABASE")
    PGPORT_ENV = os.getenv("PGPORT", "5432") # Default PostgreSQL port

    # Diagnostic logging (can be removed after confirming the fix)
    logger.info(f"get_db_connection: Read PGHOST_ENV: '{PGHOST_ENV}'")
    logger.info(f"get_db_connection: Read PGUSER_ENV: '{PGUSER_ENV}'")
    # logger.info(f"get_db_connection: Read PGPASSWORD_ENV: '{'********' if PGPASSWORD_ENV else 'None'}'") # Mask password
    logger.info(f"get_db_connection: Read PGDATABASE_ENV: '{PGDATABASE_ENV}'")
    logger.info(f"get_db_connection: Read PGPORT_ENV: '{PGPORT_ENV}'")

    local_database_url = None
    if PGHOST_ENV and PGUSER_ENV and PGPASSWORD_ENV and PGDATABASE_ENV:
        db_host = PGHOST_ENV
        local_database_url = f"postgresql://{PGUSER_ENV}:{PGPASSWORD_ENV}@{db_host}:{PGPORT_ENV}/{PGDATABASE_ENV}"
        logger.info(f"get_db_connection: Constructed DATABASE_URL for host: {db_host}")
    else:
        logger.error("get_db_connection: Insufficient PG* vars (PGHOST, PGUSER, PGPASSWORD, PGDATABASE) found.")
    
    if not local_database_url:
        logger.error("Cannot connect to DB: DATABASE_URL could not be constructed or is not configured.")
        # This specific detail will be shown to the frontend if this path is taken.
        raise HTTPException(status_code=500, detail="Database configuration error due to missing connection details in backend environment.")
    
    try:
        conn = await asyncpg.connect(local_database_url)
        # Avoid logging the full URL with password in production if possible, or just the host part
        logger.info(f"DB Connected to host: {local_database_url.split('@')[-1].split('/')[0] if '@' in local_database_url else 'DB'}")
        return conn
    except asyncpg.PostgresError as dbe:
        logger.error(f"DB Connection Failed (asyncpg.PostgresError): {dbe}")
        raise HTTPException(status_code=500, detail=f"Database connection error: {dbe}")
    except Exception as e:
        logger.error(f"DB Connection Failed (General Exception): {e}")
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

# New Endpoints using PostgreSQL
@router.post("/initialize_game", response_model=List[MemeDataWithLocalURL])
async def initialize_game_data_with_local_urls(game_request: GameInitRequest, http_request: Request):
    level = game_request.level
    num_memes_to_fetch = 0
    if level == 1:
        num_memes_to_fetch = 6
    elif level == 2:
        num_memes_to_fetch = 25
    else:
        raise HTTPException(status_code=400, detail="Invalid game level specified. Must be 1 or 2 for standard game setup.")

    conn = None
    try:
        conn = await get_db_connection()
        # Fetch necessary fields from 'meme_fetch'. No need for original image_url for serving.
        query = """
            SELECT image_name, humour, sarcasm, offensive, motivational, overall_sentiment
            FROM meme_fetch
            WHERE image_name IS NOT NULL AND image_name <> ''
            ORDER BY RANDOM()
            LIMIT $1
        """
        db_records = await conn.fetch(query, num_memes_to_fetch)
        
        if not db_records or len(db_records) < num_memes_to_fetch:
            logger.warning(f"DB: Retrieved {len(db_records)}/{num_memes_to_fetch} memes from 'meme_fetch' for level {level}.")
            if not db_records:
                 raise HTTPException(status_code=404, detail="Not enough memes in 'meme_fetch' DB for game setup.")
        
        processed_memes_data: List[MemeDataWithLocalURL] = []
        meme_id_counter = 1 
        base_url = str(http_request.base_url).rstrip('/')

        for record in db_records:
            image_name_from_db = record["image_name"]
            
            # Verify the image file actually exists in our downloaded image directory
            expected_image_path = MEME_IMAGE_DIR / image_name_from_db
            if not expected_image_path.is_file():
                logger.warning(f"Image file not found in backend storage for '{image_name_from_db}' at path '{expected_image_path}'. Skipping this meme.")
                continue # Skip this meme if its image isn't found locally
            
            # Construct the new image URL pointing to our backend serving endpoint
            local_image_url = f"{base_url}/api/games/memory_match/images/{image_name_from_db}"
            
            processed_memes_data.append(MemeDataWithLocalURL(
                id=meme_id_counter, 
                image_name=image_name_from_db,
                image_url=local_image_url, 
                text=str(record["text_corrected"] or f"Meme {meme_id_counter}"),
                humour=record["humour"],
                sarcasm=record["sarcasm"],
                offensive=record["offensive"],
                motivational=record["motivational"],
                overall_sentiment=record["overall_sentiment"]
            ))
            meme_id_counter += 1
        
        if not processed_memes_data and db_records: # All fetched records had missing image files
            logger.error(f"Fetched {len(db_records)} records from DB, but all corresponding image files were missing from {MEME_IMAGE_DIR}.")
            raise HTTPException(status_code=500, detail="Meme data found, but image files are missing in backend storage.")
        elif not processed_memes_data:
             # This case is hit if initial db_records was empty AND less than num_memes_to_fetch
             # The earlier check for len(db_records) < num_memes_to_fetch would have already caught this if db_records was totally empty.
             # So, this is more of a safeguard or if the logic above changes.
             logger.warning("No processable meme data after checking file existence.")
             # Re-evaluate if a 404 is more appropriate here as well.
             # For now, sticking to the logic that it implies an issue if initial fetch was okay but then all files missing.

        logger.info(f"Returning {len(processed_memes_data)} meme data objects (from 'meme_fetch' with local URLs) for level {level}.")
        return processed_memes_data
        
    except asyncpg.PostgresError as dbe:
        logger.error(f"DB query error on 'meme_fetch': {dbe}")
        raise HTTPException(status_code=500, detail=f"Database error: {dbe}")
    except HTTPException: 
        raise
    except Exception as e:
        logger.error(f"Unexpected error in initialize_game_data_with_local_urls (targeting 'meme_fetch'): {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected server error: {e}")
    finally:
        if conn and not conn.is_closed():
            await conn.close()

# --- New Endpoint to Serve Images --- 
@router.get("/images/{image_filename}")
async def serve_meme_image(image_filename: str):
    try:
        # Sanitize filename to prevent directory traversal - basic check
        if ".." in image_filename or image_filename.startswith("/"):
            raise HTTPException(status_code=400, detail="Invalid image filename.")

        image_path = MEME_IMAGE_DIR / image_filename
        
        if not image_path.is_file():
            logger.error(f"Image serving: File not found at {image_path}")
            raise HTTPException(status_code=404, detail="Image not found.")
        
        media_type = "image/jpeg" # Default
        if image_filename.lower().endswith(".png"):
            media_type = "image/png"
        elif image_filename.lower().endswith(".gif"):
            media_type = "image/gif"
        elif image_filename.lower().endswith(".jpg") or image_filename.lower().endswith(".jpeg"):
            media_type = "image/jpeg"
        # Add more as needed: webp, etc.

        logger.info(f"Serving image: {image_filename} from {image_path} with media type {media_type}")
        return FileResponse(str(image_path), media_type=media_type)
    except HTTPException:
        raise 
    except Exception as e:
        logger.error(f"Error serving image {image_filename}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error serving image.")

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
    # required_columns = ['image_name', 'text_corrected', 'overall_sentiment']
    required_columns = ['image_name']

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
            # 'text': row.get('text_corrected', ''),
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