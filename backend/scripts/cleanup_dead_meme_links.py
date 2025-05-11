import asyncio
import asyncpg
import aiohttp
import os
import logging
from typing import List, Tuple

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

ORIGINAL_TABLE_NAME = "meme_fetch"
CLEANED_TABLE_NAME = "meme_fetch_cleaned"

# --- Database Connection ---
async def get_db_connection_pool():
    PGHOST_ENV = os.getenv("PGHOST")
    PGUSER_ENV = os.getenv("PGUSER")
    PGPASSWORD_ENV = os.getenv("PGPASSWORD")
    PGDATABASE_ENV = os.getenv("PGDATABASE")
    PGPORT_ENV = os.getenv("PGPORT", "5432")

    if not (PGHOST_ENV and PGUSER_ENV and PGPASSWORD_ENV and PGDATABASE_ENV):
        logger.error("Database environment variables (PGHOST, PGUSER, PGPASSWORD, PGDATABASE) are not fully set.")
        raise ConnectionError("Missing database configuration in environment.")

    dsn = f"postgresql://{PGUSER_ENV}:{PGPASSWORD_ENV}@{PGHOST_ENV}:{PGPORT_ENV}/{PGDATABASE_ENV}"
    
    try:
        pool = await asyncpg.create_pool(dsn=dsn, min_size=1, max_size=5)
        logger.info(f"Successfully connected to database: {PGDATABASE_ENV} on {PGHOST_ENV}")
        return pool
    except Exception as e:
        logger.error(f"Failed to create database connection pool: {e}")
        raise

# --- URL Connectivity Check ---
async def is_url_alive(session: aiohttp.ClientSession, url: str, timeout_seconds: int = 10) -> bool:
    if not url or not url.startswith(('http://', 'https://')):
        logger.warning(f"Skipping invalid URL: {url}")
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
        logger.warning(f"URL client error ({type(e).__name__}): {url} - {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error checking URL {url}: {e}")
        return False
    return False

# --- Main Logic ---
async def main():
    pool = None
    dead_link_image_names: List[str] = []  # Changed from dead_link_ids to reflect usage of image_name

    try:
        pool = await get_db_connection_pool()
        
        async with pool.acquire() as conn:
            table_exists_check = await conn.fetchval(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = $1)",
                CLEANED_TABLE_NAME
            )

            if not table_exists_check:
                logger.info(f"Table '{CLEANED_TABLE_NAME}' does not exist. Creating it as a copy of '{ORIGINAL_TABLE_NAME}'...")
                await conn.execute(f"CREATE TABLE {CLEANED_TABLE_NAME} (LIKE {ORIGINAL_TABLE_NAME} INCLUDING ALL)")
                await conn.execute(f"INSERT INTO {CLEANED_TABLE_NAME} SELECT * FROM {ORIGINAL_TABLE_NAME}")
                logger.info(f"Table '{CLEANED_TABLE_NAME}' created and populated successfully.")
            else:
                logger.info(f"Table '{CLEANED_TABLE_NAME}' already exists. Proceeding with existing data in it.")

            # Fetch image_name and image_url from the CLEANED_TABLE_NAME
            records = await conn.fetch(f"SELECT image_name, image_url FROM {CLEANED_TABLE_NAME} WHERE image_url IS NOT NULL AND image_url <> ''")
            logger.info(f"Fetched {len(records)} records from '{CLEANED_TABLE_NAME}' table.")

        if not records:
            logger.info(f"No records with image_url found in '{CLEANED_TABLE_NAME}' to check.")
            return

        conn_config = aiohttp.TCPConnector(limit_per_host=10, limit=100, ssl=False)
        async with aiohttp.ClientSession(connector=conn_config) as session:
            tasks = []
            for record in records:
                image_name_val = record['image_name'] # Use image_name as the identifier
                image_url = record['image_url']
                tasks.append(check_and_collect_dead_link(session, image_name_val, image_url, dead_link_image_names))
            
            await asyncio.gather(*tasks)

        logger.info(f"Found {len(dead_link_image_names)} dead links out of {len(records)} checked URLs in '{CLEANED_TABLE_NAME}'.")

        if dead_link_image_names:
            logger.info(f"Preparing to delete {len(dead_link_image_names)} records from '{CLEANED_TABLE_NAME}'...")
            async with pool.acquire() as conn:
                # Use image_name (text) for deletion
                deleted_count_result = await conn.execute(
                    f"DELETE FROM {CLEANED_TABLE_NAME} WHERE image_name = ANY($1::text[])", 
                    dead_link_image_names
                )
                logger.info(f"Successfully deleted records from '{CLEANED_TABLE_NAME}'. Result: {deleted_count_result}") 
        else:
            logger.info(f"No dead links found to delete from '{CLEANED_TABLE_NAME}'.")

    except ConnectionError:
        logger.error("Could not establish database connection. Aborting.")
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
    finally:
        if pool:
            await pool.close()
            logger.info("Database connection pool closed.")

async def check_and_collect_dead_link(session, image_name_val, image_url, dead_link_list):
    is_alive = await is_url_alive(session, image_url)
    if not is_alive:
        dead_link_list.append(image_name_val) # Store image_name instead of id
    
if __name__ == "__main__":
    asyncio.run(main())
