import asyncio
import aiohttp # For asynchronous HTTP requests
import os
import logging
import csv # For CSV handling
from typing import List, Dict, Any

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# === Configuration for Double-Checking ===
INPUT_CSV_FILE = "backend/datasets/meme_cleand_202505112225.csv" # Input is the previously cleaned file
OUTPUT_CSV_FILE = "backend/datasets/meme_links_double_checked.csv" # New output for the double-check results

EXPECTED_COLUMNS = [
    'image_name', 'text_ocr', 'text_corrected', 'humour', 'sarcasm', 
    'offensive', 'motivational', 'overall_sentiment', 'original_name', 'image_url'
]
# EXPECTED_DATA_ROWS = 6992 # Commented out for double-check, as row count will be different
IMAGE_URL_COLUMN = 'image_url' # The column containing the URLs to check

# --- URL Connectivity Check (remains largely the same) ---
async def is_url_alive(session: aiohttp.ClientSession, url: str, timeout_seconds: int = 10) -> bool:
    if not url or not isinstance(url, str) or not url.startswith(('http://', 'https://')):
        logger.warning(f"Skipping invalid or non-string URL: '{url}'")
        return False
    try:
        async with session.head(url, timeout=timeout_seconds, allow_redirects=True) as response:
            if 200 <= response.status < 300:
                return True
            else:
                logger.warning(f"URL dead (HEAD Status {response.status}): {url}")
                return False
    except asyncio.TimeoutError:
        logger.warning(f"URL timed out: {url}")
        return False
    except aiohttp.ClientError as e:
        logger.warning(f"URL client error ({type(e).__name__} for {url}): {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error checking URL {url}: {e}")
        return False
    return False

# --- Main Logic ---
async def main():
    all_rows_from_csv: List[Dict[str, Any]] = []
    live_link_rows: List[Dict[str, Any]] = []

    # --- 1. Read and Validate CSV --- 
    logger.info(f"Attempting to read CSV file for double-checking: {INPUT_CSV_FILE}")
    if not os.path.exists(INPUT_CSV_FILE):
        logger.error(f"Input CSV file not found: {INPUT_CSV_FILE}")
        return

    try:
        with open(INPUT_CSV_FILE, mode='r', encoding='utf-8', newline='') as infile:
            reader = csv.DictReader(infile)
            actual_columns = reader.fieldnames
            
            if actual_columns is None:
                logger.error(f"Could not read header from CSV: {INPUT_CSV_FILE}. File might be empty or malformed.")
                return
                
            logger.info(f"CSV Columns found: {actual_columns}")
            if list(actual_columns) != EXPECTED_COLUMNS:
                logger.error(f"CSV column mismatch! Expected: {EXPECTED_COLUMNS}, Found: {actual_columns}")
                missing_cols = set(EXPECTED_COLUMNS) - set(actual_columns)
                extra_cols = set(actual_columns) - set(EXPECTED_COLUMNS)
                if missing_cols:
                    logger.error(f"Missing expected columns: {missing_cols}")
                if extra_cols:
                    logger.error(f"Found unexpected extra columns: {extra_cols}")
                logger.error("Please ensure the CSV schema matches the expected structure.")
                return
            logger.info("CSV schema validation successful.")

            all_rows_from_csv = list(reader)
            num_data_rows = len(all_rows_from_csv)
            logger.info(f"Read {num_data_rows} data rows from CSV ({INPUT_CSV_FILE}).")

            # Row Count Validation - now just a log, not a hard stop
            # if num_data_rows != EXPECTED_DATA_ROWS:
            #     logger.warning(f"Row count mismatch. Expected: {EXPECTED_DATA_ROWS} data rows, Found: {num_data_rows} data rows.")
            # else:
            #     logger.info("CSV row count validation successful.")

    except FileNotFoundError:
        logger.error(f"Input CSV file not found: {INPUT_CSV_FILE}")
        return
    except Exception as e:
        logger.error(f"Error reading or validating CSV file {INPUT_CSV_FILE}: {e}", exc_info=True)
        return

    if not all_rows_from_csv:
        logger.info("No data rows found in CSV to process.")
        return

    # --- 2. Check URL Connectivity --- 
    logger.info(f"Starting URL connectivity double-check for {len(all_rows_from_csv)} rows...")
    conn_config = aiohttp.TCPConnector(limit_per_host=20, limit=100, ssl=False)
    async with aiohttp.ClientSession(connector=conn_config) as session:
        tasks = []
        for row_index, row_data in enumerate(all_rows_from_csv):
            image_url_to_check = row_data.get(IMAGE_URL_COLUMN)
            tasks.append(check_url_and_collect_row(session, row_index, row_data, image_url_to_check, live_link_rows))
        
        await asyncio.gather(*tasks)
    
    num_live_links = len(live_link_rows)
    num_dead_links = len(all_rows_from_csv) - num_live_links
    logger.info(f"URL Connectivity Double-Check Complete. Total rows processed: {len(all_rows_from_csv)}, Live links found: {num_live_links}, Dead links found this run: {num_dead_links}")

    # --- 3. Write Double-Checked Data to New CSV --- 
    if live_link_rows:
        logger.info(f"Writing {num_live_links} rows with validated live links to {OUTPUT_CSV_FILE}...")
        try:
            with open(OUTPUT_CSV_FILE, mode='w', encoding='utf-8', newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=EXPECTED_COLUMNS)
                writer.writeheader()
                writer.writerows(live_link_rows)
            logger.info(f"Successfully wrote double-checked data to {OUTPUT_CSV_FILE}")
        except Exception as e:
            logger.error(f"Error writing double-checked CSV to {OUTPUT_CSV_FILE}: {e}", exc_info=True)
    else:
        logger.info("No live links found in this double-check run. Output CSV file will not be created or will be empty.")

async def check_url_and_collect_row(session, row_idx, row_data_dict, image_url, live_link_rows_list):
    is_alive = await is_url_alive(session, image_url)
    if is_alive:
        live_link_rows_list.append(row_data_dict)
    else:
        # Log which image_name has a dead link
        image_name = row_data_dict.get('image_name', '[image_name_not_found]') # Get image_name, provide fallback
        logger.warning(f"Dead link identified for image_name: '{image_name}'. URL: {image_url}")
    
if __name__ == "__main__":
    output_dir = os.path.dirname(OUTPUT_CSV_FILE)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info(f"Created output directory: {output_dir}")

    asyncio.run(main())
